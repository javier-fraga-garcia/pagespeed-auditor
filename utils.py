import concurrent.futures as fs
import requests
import re
import csv
from collections import defaultdict
from tqdm.auto import tqdm

def get_urls(urls_file, domain='https://'):
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
    results = defaultdict(None, **{'crux_cumulative_layout_shift': None, 'crux_experimental_interaction_next_paint': None, 'crux_experimental_time_first_byte': None, 'crux_first_contentful_paint': None, 'crux_first_input_delay': None, 'crux_largest_contentful_paint': None, 'crux_overall': None})

    results['final_url'] = audit['lighthouseResult']['finalUrl']
    results['device'] = audit['lighthouseResult']['configSettings']['emulatedFormFactor']
    results['first_contentful_paint'] = float(re.sub('[a-zA-Z_,]', '', audit['lighthouseResult']['audits']['first-contentful-paint']['displayValue']).strip()) if 'first-contentful-paint' in audit['lighthouseResult']['audits'] else None
    results['time_to_interactive'] = float(re.sub('[a-zA-Z_,]', '', audit['lighthouseResult']['audits']['interactive']['displayValue']).strip()) if 'interactive' in audit['lighthouseResult']['audits'] else None
    results['largest_contentful_paint'] = float(re.sub('[a-zA-Z_,]', '', audit['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']).strip()) if 'largest-contentful-paint' in audit['lighthouseResult']['audits'] else None
    results['speed_index'] = float(re.sub('[a-zA-Z_,]', '', audit['lighthouseResult']['audits']['speed-index']['displayValue']).strip()) if 'speed-index' in audit['lighthouseResult']['audits'] else None
    results['total_blocking_time'] = float(re.sub('[a-zA-Z_,]', '', audit['lighthouseResult']['audits']['total-blocking-time']['displayValue']).strip()) if 'total-blocking-time' in audit['lighthouseResult']['audits'] else None
    results['dom_size'] = int(re.sub('[a-zA-Z_,]', '', audit['lighthouseResult']['audits']['dom-size']['displayValue']).strip()) if 'dom-size' in audit['lighthouseResult']['audits'] else None
    results['performance'] = audit['lighthouseResult']['categories']['performance']['score'] if 'performance' in audit['lighthouseResult']['categories'] else None
    results['accessibility'] = audit['lighthouseResult']['categories']['accessibility']['score'] if 'accessibility' in audit['lighthouseResult']['categories'] else None
    results['best_practices'] = audit['lighthouseResult']['categories']['best-practices']['score'] if 'best-practices' in audit['lighthouseResult']['categories'] else None
    results['seo'] = audit['lighthouseResult']['categories']['seo']['score'] if 'seo' in audit['lighthouseResult']['categories'] else None

    if 'metrics' in audit['loadingExperience']:
      results['crux_cumulative_layout_shift'] = audit['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['category'] if 'CUMULATIVE_LAYOUT_SHIFT_SCORE' in audit['loadingExperience']['metrics'] else None
      results['crux_experimental_interaction_next_paint'] = audit['loadingExperience']['metrics']['EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT']['category'] if 'EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT' in audit['loadingExperience']['metrics'] else None
      results['crux_experimental_time_first_byte'] = audit['loadingExperience']['metrics']['EXPERIMENTAL_TIME_TO_FIRST_BYTE']['category'] if 'EXPERIMENTAL_TIME_TO_FIRST_BYTE' in audit['loadingExperience']['metrics'] else None
      results['crux_first_contentful_paint'] = audit['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category'] if 'FIRST_CONTENTFUL_PAINT_MS' in audit['loadingExperience']['metrics'] else None
      results['crux_first_input_delay'] = audit['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['category'] if 'FIRST_INPUT_DELAY_MS' in audit['loadingExperience']['metrics'] else None
      results['crux_largest_contentful_paint'] = audit['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['category'] if 'LARGEST_CONTENTFUL_PAINT_MS' in audit['loadingExperience']['metrics'] else None
      results['crux_overall'] = audit['loadingExperience']['overall_category'] if 'overall_category' in audit['loadingExperience'] else None

    return results

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
      audit = response.json()
      return parse_audit(audit)
  except:
    print(f'[!] Something went wrong with {url}')

def make_audits(urls, api_key, strategy, verbose=False):
  print(f'[+] Auditing {len(urls)} unique URLs\n')
  audits = [make_audit(url, api_key, strategy, verbose) for url in tqdm(urls, position=0, leave=True)]
  return [audit for audit in audits if audit is not None]

def make_parallel_audits(urls, api_key, strategy, max_workers=5, verbose=False):
  print(f'[+] Auditing {len(urls)} unique URLs\n')
  with fs.ThreadPoolExecutor(max_workers=max_workers) as exec:
    futures = [exec.submit(make_audit, url, api_key, strategy, verbose) for url in urls]
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