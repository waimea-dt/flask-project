# Lang Test

```simple
# Simple language demo for highlight.js
# initialize and loop
do
  count = 0
  while count < 5
    # show a message (pseudo-IO)
    msg = "Iteration " + count
    count = count + 1
  end

  if count >= 5
    return "finished"
  else
    return "not_finished"
  end
end
```
