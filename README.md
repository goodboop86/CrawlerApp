Crawler App

```mermaid
sequenceDiagram
    Alice->>+John: Hello John, how are you?
    Alice->>+John: John, can you hear me?
    John-->>-Alice: Hi Alice, I can hear you!
    John-->>-Alice: I feel great!
```


```
cd fastapi
uvicorn back:app --reload
```

```
cd streamlit
streamlit run front.py
```