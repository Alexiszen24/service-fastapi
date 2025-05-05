from fastapi import Body


example_create_line = Body(
    openapi_examples={
        "normal":   {
            "summary": "Типовой запрос",
            "description": "Типовой запрос для создания линии",
            "value": {
                "name": "L-01",
                "status": "offline",
            }
        },
        "invalid": {
            "summary": "Некорректные данные",
            "value": {
                "name": "L-01",
                "status": "online-32",
            },
        },
    }
)