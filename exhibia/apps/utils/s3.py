html = """
<html>
  <head>
    <title>S3 POST Form</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>

  <body>
    <form action="https://%(bucket)s.s3.amazonaws.com/" method="post" enctype="multipart/form-data">
      <input type="hidden" name="key" value="uploads/${filename}">
      <input type="hidden" name="AWSAccessKeyId" value="%(aws_key)s">
      <input type="hidden" name="acl" value="private">
      <input type="hidden" name="success_action_redirect" value="http://testing.exhibia.com:8000/">
      <input type="hidden" name="policy" value="%(policy)s">
      <input type="hidden" name="signature" value="%(signature)s">
      <input type="hidden" name="Content-Type" value="image/jpeg">
      <input type="hidden" name="x-amz-meta-auction" value="44444">
      <input type="hidden" name="x-ignore-auction" value="44444">

      <!-- Include any additional input fields here -->

      File to upload to S3:
      <input name="file" type="file">
      <br>
      <input type="submit" value="Upload File to S3">
    </form>
  </body>
</html>
"""
import base64
import hmac, sha

def generate_form():
    AWS_KEY = 'AKIAJ4PKN5RE7BF557BA'
    AWS_SECRET_KEY = """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"""
    bucket_name = "videuploadertest1"

    policy_document = """{"expiration": "2013-01-01T00:00:00Z",
      "conditions": [
        {"bucket": "videuploadertest1"},
        ["starts-with", "$key", "uploads/"],
        {"acl": "private"},
        {"success_action_redirect": "http://testing.exhibia.com:8000/"},
        ["starts-with", "$Content-Type", ""],
        ["content-length-range", 0, 1048576]
      ]
    }"""
    policy = base64.b64encode(policy_document).replace("\n","")

    signature = base64.b64encode(
        hmac.new(AWS_SECRET_KEY, policy, sha).digest()).replace("\n","")


    return html %({'aws_key':AWS_KEY,
                   'policy':policy,
                   'signature':signature,
                   'bucket':bucket_name})