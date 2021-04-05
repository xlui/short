# short

![GitHub](https://img.shields.io/github/license/xlui/short.svg)

A URL shortener.

## Usage

Install and run:

```bash
pip install -r requirements.txt
python app.py
```

Encode:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"url": "www.google.com", "code": "g"}' localhost:5000/encode
```

```
{"code":0,"data":"http://127.0.0.1:5000/g","error":null}
```

Decode:

```shell
curl http://127.0.0.1:5000/g
```

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="www.google.com">www.google.com</a>.  If not click the link.
```

## License

[MIT](LICENSE)
