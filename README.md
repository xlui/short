# short

![GitHub](https://img.shields.io/github/license/xlui/short.svg)

Server-side URL shorten code. This system also supports customize short code. 

No front end now, I don't have much energy now. UI maybe added in some day of the future.

## Algorithm

1. Determine customize or not. If customize, go to 2, else go to 3.
2. Check chosen code has been used or not. If used, return error, else save new record and return success.
3. Add a new record and generate code using the id of new record.
4. Check generated code has been used or not. If used, regenerate code using the conflict record's id. If not used,
update code field of the record.

The reason why we use conflict record's id to regenerate code is that there is only one certain sort of situation will
cause conflict. Only when user choose to use customized code, customized code may cause conflict with system generated
code. And the id of conflict record has not been used to generate code, so for the new record, we can just use the
conflict record's id.

## How to run

First, install all requirements:

```bash
pip install -r requirements.txt
```

Next, run the project and generate database file:

```bash
python app.py
curl localhost:5000/
```

Then you can visit the two APIs provided by this system.

### Encode

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "www.google.com", "code": "g"}' localhost:5000/encode
```

`code` field in JSON is optional. If present, the system will try to use code as short code(If this code have not been used). If not present, the system will generate short code with record's id.

The response:

```
{
  "code": 0,
  "data": "g",
  "error": null
}
```

### Decode

```bash
curl -X POST -H "Content-Type: application/json" -d '{"code": "g"}' localhost:5000/decode
```

The response:

```
{
  "code": 0,
  "data": {
    "url": "www.google.com"
  },
  "error": null
}
```
