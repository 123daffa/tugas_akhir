from app.models.groq_vision import groq_vision_handler


caption = groq_vision_handler.generate_caption(
    "pertamina-1.jpg"
)


print("======================")
print("IMAGE DESCRIPTION")
print("======================")

print(caption)