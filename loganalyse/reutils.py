import re
import json
import os


#匹配日志，返回一个字典
def get_log_dict(log_line):
    # plaintext
    LOG_FORMAT = '$remote_addr $user_realip $remote_user $server_addr [$time_iso8601] $scheme $host "$request" $status $request_time $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for" "$upstream_addr" "$upstream_response_time" -'

    supplied_fields = LOG_FORMAT.replace('[', '').replace(']', '').replace('"', '').split()

    # 利用非贪婪匹配和分组匹配(plaintext格式需要)
    ngx_style_log_field_pattern = {
        '$remote_addr': '(?P<remote_addr>.*?)',
        '$user_realip': '(?P<user_realip>.*?)',
        '$time_local': '(?P<time_local>.*?)',
        '$time_iso8601': '(?P<time_iso8601>.*?)',
        '$server_addr': '(?P<server_addr>.*?)',
        '$request': '(?P<request>.*?)',
        '$upstream_response_time': '(?P<upstream_response_time>.*?)',
        '$upstream_addr': '(?P<upstream_addr>.*?)',
        '$request_method': '(?P<request_method>GET|POST|HEAD|DELETE|PUT|OPTIONS|CONNECT)',
        '$status': '(?P<status>.*?)',
        '$body_bytes_sent': '(?P<body_bytes_sent>.*?)',
        '$request_time': '(?P<request_time>.*?)',
        '$http_referer': '(?P<http_referer>.*?)',
        '$http_user_agent': '(?P<http_user_agent>.*?)',
        '$http_x_forwarded_for': '(?P<http_x_forwarded_for>.*)',
        '$scheme': '(?P<scheme>.*?)',
        '$request_uri': '(?P<request_uri>.*?)',
        '$uri': '(?P<uri>.*?)',
        '$document_uri': '(?P<uri>.*?)',
        '$args': '(?P<args>.*?)',
        '$query_string': '(?P<args>.*?)',
        '$server_protocol': '(?P<server_protocol>.*?)',
        '$server_name': '(?P<http_host>.*?)',
        '$host': '(?P<http_host>.*?)',
        '$http_host': '(?P<http_host>.*?)',
        '$request_length': '(?P<request_length>.*?)',
        '$remote_user': '(?P<remote_user>.*?)',
        '$gzip_ratio': '(?P<gzip_ratio>.*?)',
        '$connection_requests': '(?P<connection_requests>.*?)'
    }
    # 通过LOG_FORMAT得到可以匹配整行日志的log_pattern
    for filed in supplied_fields:
        if filed in ngx_style_log_field_pattern:
            LOG_FORMAT = LOG_FORMAT.replace(filed, ngx_style_log_field_pattern[filed], 1)
    log_pattern = LOG_FORMAT.replace('[', '\\[').replace(']', '\\]')

    # $request的正则, 其实是由 "request_method request_uri server_protocol"三部分组成
    request_uri_pattern = r'^(?P<request_method>GET|POST|HEAD|DELETE|PUT|OPTIONS|CONNECT) ' \
                        r'(?P<request_uri>.*?) ' \
                        r'(?P<server_protocol>.*)$'

    log_pattern_obj = re.compile(log_pattern)
    request_uri_pattern_obj = re.compile(request_uri_pattern)

    #匹配一行日志
    log_pattern_result = log_pattern_obj.match(log_line)
    #匹配request参数
    request_uri_pattern_result = request_uri_pattern_obj.match(log_pattern_result['request'])

    # 结果字典
    result_dict = log_pattern_result.groupdict()
    result_dict.update(request_uri_pattern_result.groupdict())

    # log_pattern_result['request_method'] = request_uri_pattern_result.groupdict('request_method')
    # log_pattern_result['request_uri'] = request_uri_pattern_result.group(1)
    # log_pattern_result['server_protocol'] = request_uri_pattern_result.group(2)

    # for item in log_pattern_result:
    #     print(item)
    # print(result_dict)
    return result_dict


# 遍历目录文件夹下的所有日志文件
# def get_log_files


# 过滤掉静态文件
def url_file_filter(_url, _status):
    filter_flag = False
    filter_url = ''

    # 状态为400的不统计
    if int(_status) == 400:
        filter_flag = True

    filter_list = ['.js', '.css', '.map', '.png', '.woff', '.woff2', '.ttf', '.ico']
    for item in filter_list:
        if _url.endswith(item):
            filter_flag = True

    if not filter_flag:
        url_last = _url.split('/')[-1:][0]
        pattern = re.compile(r'[0-9]+')
        match = pattern.findall(url_last)
        if match:
            filter_flag = True
            filter_url = _url[0:_url.rindex('/')]
        else:
            filter_url = _url
    return filter_flag, filter_url


if __name__ == '__main__1':
    book_path = 'D:\\xiezhonghai\\Desktop\\grouppurchaselog\\'
    lists = [x for x in os.listdir(book_path) if x.find('access.log') > -1]

    for item in lists:
        print(os.path.join(book_path, item))

if __name__ == '__main__':

    interface_list = {'/goDrugstoreIndex'}

    book_path = 'D:\\xiezhonghai\\Desktop\\grouppurchaselog\\'
    # 获取目录下所有的日志文件
    log_path_list = [x for x in os.listdir(book_path) if x.find('access.log') > -1]

    # 结果集
    result = {}

    for log_path in log_path_list:
        with open(os.path.join(book_path, log_path), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line_dict = get_log_dict(line)

                status = line_dict['status']
                url_key = line_dict['request_uri'].split('?')[0]
                filter_flag, filter_url = url_file_filter(url_key, status)

                url_key = filter_url + '-' + line_dict['request_method']

                if not filter_flag and not len(filter_url) == 0:
                    request_time = round(float(line_dict['request_time']), 3)
                    # response_time = round(float(line_dict['upstream_response_time']), 3)
                    if url_key not in result.keys():
                        result[url_key] = {}
                        result[url_key]['request_count'] = 1
                        result[url_key]['request_time'] = request_time
                        result[url_key]['request_avg_time'] = request_time
                        result[url_key]['request_max_time'] = request_time
                        result[url_key]['request_min_time'] = request_time

                        # result[url_key]['response_time'] = response_time
                    else:
                        result[url_key]['request_count'] = int(result[url_key]['request_count']) + 1
                        result[url_key]['request_time'] = round(result[url_key]['request_time'] + request_time, 3)
                        result[url_key]['request_avg_time'] = round(result[url_key]['request_time'] / result[url_key]['request_count'], 3)
                        result[url_key]['request_max_time'] = (request_time if (request_time > result[url_key]['request_max_time']) else
                                                               result[url_key]['request_max_time'])
                        result[url_key]['request_min_time'] = (request_time if (request_time < result[url_key]['request_max_time']) else
                                                               result[url_key]['request_max_time'])
        print('已处理文件：%s' % os.path.split(log_path)[1])

    # 返回排序后的dict元组
    result_sort_dict_list = [(k, result[k]) for k in sorted(result.keys())]

    # 写入结果文件
    with open('D:\\xiezhonghai\\Desktop\\grouppurchaselog\\log_result.md', 'a', encoding='utf-8') as f:
        f.writelines('|接口url  | 请求方式  | 请求次数 |  请求时间(s) |  平均请求时间(s)|\n')
        f.writelines('| ---- | ---- | ---- | ---- |\n')
        for key, value in result_sort_dict_list:
            f.writelines('|%s |  %s  |  %s |  %s  | %s|\n' %
                         (key.split('-')[0], key.split('-')[1], value['request_count'], value['request_time'], value['request_avg_time']))

        f.writelines('---\n')
        f.writelines('统计文件：\n')
        for log_path in log_path_list:
            f.writelines('\t' + os.path.split(log_path)[1] + '\n')

    print('日志文件全部处理完成')