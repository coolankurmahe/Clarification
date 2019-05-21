## Building
```docker build -t clarification .```

## Running
```docker run --rm -it -p5000:5000 clarification```

## Pushing
```
docker tag clarification gcr.io/development-172712/clarification
docker push gcr.io/development-172712/clarification
```

