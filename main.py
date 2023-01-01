import argparse
import time
from utils import get_urls, get_api_key, make_audits, make_concurrent_audits, write_results


def get_time(callback=None):
    def wrapper():
        start = time.perf_counter()
        callback()
        print(f'[+] Program execution has taken {(time.perf_counter() - start):.4f} seconds.')
    return wrapper

@get_time
def main():
    parser = argparse.ArgumentParser(prog = 'PageSpeed Auditor', description = 'A script to automate WebVitals audits via the PageSpeed API')
    parser.add_argument('-u', '--urls', type=str, help='the path to the file containing the URLs to be audited')
    parser.add_argument('-k', '--key', type=str, help='the path to the file containing the PageSpeed API key')
    parser.add_argument('-s', '--strategy', type=str, choices=['desktop', 'mobile'], help='the device on which to perform the WebVitals audit')
    parser.add_argument('-d', '--domain', type=str, help='the domain under which the audit is to be performed')
    parser.add_argument('-r', '--result', type=str, help='the name of the results file')
    parser.add_argument('-c', '--concurrent', default=False, action='store_true', help='(optional) if you wish to perform multithreaded audits')

    args = parser.parse_args()
    urls = args.urls
    key = args.key
    strategy = args.strategy
    domain = args.domain
    result = args.result
    concurrent = args.concurrent

    urls = get_urls(urls, domain)
    api_key = get_api_key(key)

    if urls and api_key:
        if not concurrent:
            audits = make_audits(urls, api_key, strategy)
            write_results(audits, result)
        else:
            audits = make_concurrent_audits(urls, api_key, strategy)
            write_results(audits, result)



if __name__ == '__main__':
    main()