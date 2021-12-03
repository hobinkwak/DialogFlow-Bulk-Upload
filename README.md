# DialogFlow-Bulk-Upload


## Intents CSV Upload 

- csv로 된 질문-답변 데이터를 DialogFlow에 업로드할 수 있도록 json포맷으로 변환
- DialogFlow의 Settings에서 Restore From ZIP 활용

## Catch Entity Automatically

- 기 작성된 Entity json파일이 있다는 전제하에
- 해당 Entity들을 여러 Intents json파일에 자동으로 덧입히기

## Usage

```python
# csv로부터 intents json 생성
main(generate_intents=True, catch_entity=False)

# entity 파일이 있다는 전제하에
main(generate_intents=False, catch_entity=True)
```
