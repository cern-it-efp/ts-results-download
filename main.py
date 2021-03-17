import requests
import argparse
import os

# -----------------FUNCTIONS----------------------------------------------------
def getOriginalFilename(resHeaders,presignedURL):
    """ Gets the original filename. Tries to do so using the response
        headers. In case of issues, takes the filename from the provided
        pre-signed URL.
    """

    try:
        return resHeaders["X-Amz-Meta-Orig-Filename"]
    except:
        return os.path.basename(presignedURL.split('?')[0])


def getFile(presignedURL, destination):
    """ Pulls an object from the bucket given its pre-signed URL and places it
        in a given destination.
    """

    # Make request
    res = requests.get(presignedURL)

    # Check response code
    if res.status_code != 200:
        return False

    # Get filename
    filename = getOriginalFilename(res.headers,presignedURL)

    # Save received file
    with open("%s/%s" % (destination,filename), 'wb') as fd:
        for chunk in res.iter_content(chunk_size=128):
            fd.write(chunk)


# -----------------CMD OPTIONS--------------------------------------------------
parser = argparse.ArgumentParser(description='Test-Suite results fetch.')
parser.add_argument('-p','--pre-signed-URLs',
                    help='Path to file listing pre-signed URLs.',
                    type=str,
                    dest="pathPresignedURLs",
                    required=True)
parser.add_argument('-d','--destination',
                    help='Location where to save fetched files.',
                    type=str,
                    dest="destination",
                    default=".")


args = parser.parse_args()

# For each URL on the list, get a file
for presignedURL in open(args.pathPresignedURLs).readlines():

    presignedURL = presignedURL.strip()

    print("Getting file from: %s..." % presignedURL[:100])

    try:
        if getFile(presignedURL,args.destination) == False:
            print("   ERROR: unable to get file from: %s..." % presignedURL[:100])
        else:
            print("   OK")
    except BaseException as ex:
        print("   ERROR: unable to get file from: %s..." % presignedURL[:100])
        print(ex)
    print(" -------- ")
