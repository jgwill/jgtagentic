#ngrok http -skip-browser-warning  --url=heartily-optimum-bobcat.ngrok-free.app 3222
#ngrok http --url=heartily-optimum-bobcat.ngrok-free.app 3000

# So we can expose our local server to the internet
ngrok http --url=$NGROK_URL_BEAGLE 3000

