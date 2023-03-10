import concurrent.futures as fs
from tqdm.auto import tqdm
import requests
import re
import csv

def get_urls(urls_file, domain):
  try:
    with open(urls_file, 'r') as f:
      return {url.strip() for url in f.read().split('\n') if len(url) > 0 and url.startswith(domain)}
  except:
    print(f'[!] File {urls_file} could not be opened')

def get_api_key(api_key_file):
  try:
    with open(api_key_file, 'r') as f:
      return f.read().strip()
  except:
    print(f'[!] File {api_key_file} could not be opened')

def parse_audit(audit):
  return {
      'final_url': audit['finalUrl'],
      'device': audit['configSettings']['emulatedFormFactor'],
      'first_contentful_paint': float(re.sub('[a-zA-Z_,]', '', audit['audits']['first-contentful-paint']['displayValue']).strip()) if audit['audits']['first-contentful-paint']['displayValue'] else None,
      'time_to_interactive': float(re.sub('[a-zA-Z_,]', '', audit['audits']['first-contentful-paint']['displayValue']).strip()) if audit['audits']['first-contentful-paint']['displayValue'] else None,
      'largest_contentful_paint': float(re.sub('[a-zA-Z_,]', '', audit['audits']['interactive']['displayValue']).strip()) if audit['audits']['interactive']['displayValue'] else None,
      'speed_index': float(re.sub('[a-zA-Z_,]', '', audit['audits']['speed-index']['displayValue']).strip()) if audit['audits']['speed-index']['displayValue'] else None,
      'total_blocking_time': float(re.sub('[a-zA-Z_,]', '', audit['audits']['total-blocking-time']['displayValue']).strip()) if audit['audits']['total-blocking-time']['displayValue'] else None,
      'dom_size': int(re.sub('[a-zA-Z_,]', '', audit['audits']['dom-size']['displayValue']).strip()) if audit['audits']['dom-size']['displayValue'] else None,
      'performance': audit['categories']['performance']['score'] if audit['categories']['performance']['score'] else None,
      'accessibility': audit['categories']['accessibility']['score'] if audit['categories']['accessibility']['score'] else None,
      'best_practices': audit['categories']['best-practices']['score'] if audit['categories']['best-practices']['score'] else None,
      'seo': audit['categories']['seo']['score'] if audit['categories']['seo']['score'] else None
  }

def make_audit(url, api_key, strategy, verbose=False):
  ENDPOINT = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&category=best-practices&category=performance&category=seo&category=accessibility&key={}'
  params = {
      'strategy': strategy
  }
  try:
    if verbose:
      print(f'[+] Auditing {url} with strategy {strategy}')
    response = requests.get(ENDPOINT.format(url, api_key), params)
    if response.status_code == 200:
      audit = response.json()['lighthouseResult']
      return parse_audit(audit)
  except:
    print(f'[!] Something went wrong with {url}')

def make_audits(urls, api_key, strategy):
  print(f'[+] Auditing {len(urls)} unique URLs\n')
  audits = [make_audit(url, api_key, strategy) for url in tqdm(urls, position=0, leave=True)]
  return [audit for audit in audits if audit is not None]

def make_parallel_audits(urls, api_key, strategy, max_workers=5):
  print(f'[+] Auditing {len(urls)} unique URLs\n')
  with fs.ThreadPoolExecutor(max_workers=max_workers) as exec:
    futures = [exec.submit(make_audit, url, api_key, strategy) for url in urls]
    audits = [future.result() for future in fs.as_completed(futures)]
  return [audit for audit in audits if audit is not None]

def write_results(audits, file_name):
  try:
    with open(f'{file_name}.csv', 'w+', newline='') as f:
      writer = csv.writer(f)
      headers = list(audits[0].keys())
      writer.writerow(headers)

      for audit in audits:
        res = [audit.get(key, None) for key in headers]
        writer.writerow(res)
      print(f'[+] Written file in {file_name}.csv\n')
  except:
    print(f'[!] Something went wrong when writing the file {file_name}')