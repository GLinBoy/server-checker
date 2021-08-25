import click
from tcp_latency import measure_latency
from heapq import nsmallest


def Average(lst):
    return sum(lst, 0.0) / len(lst)


@click.command()
@click.option('-p', '--path', default='ips.txt', help='File path (Default: ips.txt)')
@click.option('-r', '--runs', default=5, help='Number of trys to get avarage (Default: 5)')
@click.option('-t', '--timeout', default=2500, help='Timeout for connection in millisecound (Default: 2500)')
@click.option('-s', '--results', default=5, help='Numebr of results to present (Default: 5)')
def testServers(path, runs, timeout, results):
    with open(path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    ips = {}
    for index, c in enumerate(content):
        latencies = list(filter(None, measure_latency(host=c, runs=runs, timeout=timeout/1000)))
        if latencies and len(latencies) > 0:
            latency = round(Average(latencies), 2)
            line = f"{index + 1:02d}. Pinged {c}; latency: {latency} ms;"
            ips[c] = latency
        else:
            line = f"{index + 1:02d}. Pinged {c}; UNKNOWN!!!"
            ips[c] = -1.00
        print(line)
    print('----------------------------------------------------------------')
    print(f'#{results} Best Servers: ')
    cleaned_ips = {k : v for k,v in ips.items() if v > 0}
    my_ips = nsmallest(results, cleaned_ips, key = cleaned_ips.get)
    for index, ip in enumerate(my_ips):
        line = f"{index + 1}. {ip}: {ips.get(ip)} ms"
        print(line)


if __name__ == '__main__':
    testServers()