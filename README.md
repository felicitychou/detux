# detux
detux.org SDK API

You can use this to search sample in detux.org and get the analysis report of sample based on its sha256.

```
usage:
        detux -k api_key -s text
        detux -k api_key -g sha256
        detux -k api_key --submit filepath
        api_key = 
        text = "*"
        sha256 = ""
param:
        -k/--apikey  api_key
        -s/--search  search text
          --from  search text from 
        -g/--getreport get report based on sha256
        --submit submit file
            --private submit file private
            --filename set file name
            --comments  set comments
        -h/--help    help
```
