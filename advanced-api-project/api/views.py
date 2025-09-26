def perform_create(self, serializer):
    # Custom behavior: Ensure the book is saved with validated data
    serializer.save()

def perform_update(self, serializer):
    # Custom behavior: Ensure updates are saved with validated data
    serializer.save()