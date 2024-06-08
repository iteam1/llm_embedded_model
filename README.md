# llm_embedded_model 

An API-based application that communicates with a large language model over a network through HTTP requests

# guide

- Run app `uvicorn main:app --reload`

- Test the API:

        curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d '{"prompt": "Once upon a time", "max_tokens": 50}'

# shout out to

[nginx-docs](https://nginx.org/en/docs/)

[alfredodeza/huggingface-deploy-azure](https://github.com/alfredodeza/huggingface-deploy-azure)
