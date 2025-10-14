from django.db.models import (
    Model,
    CharField,
    TextField,
    ForeignKey,
    OneToOneField,
    ManyToManyField,
    ManyToOneRel,
    ManyToManyRel,
)
from typing import Type, List, Set


def get_string_fields(
    model: Type[Model],
    prefix: str = "",
    depth: int = 1,
    visited=None,
) -> List[str]:
    """
    Recursively collects all string fields from a Django model,
    including nested fields from related models up to a given depth.
    Excludes fields containing 'password'.
    Prevents infinite loops by tracking visited models.
    """
    if visited is None:
        visited = set()

    if depth == 0:
        return []

    # Prevent revisiting the same model
    if model in visited:
        return []

    visited.add(model)
    fields = []

    for field in model._meta.get_fields():
        # Skip auto-created fields unless they are reverse relations
        if field.auto_created and not isinstance(field, (ManyToOneRel, ManyToManyRel)):
            continue

        # Direct string fields
        if isinstance(field, (CharField, TextField)) and "password" not in field.name:
            fields.append(f"{prefix}{field.name}")

        # Forward relations
        elif isinstance(field, (ForeignKey, OneToOneField, ManyToManyField)):
            related_model = field.related_model
            if isinstance(related_model, type) and issubclass(related_model, Model):
                nested_prefix = f"{prefix}{field.name}__"
                fields.extend(
                    get_string_fields(related_model, nested_prefix, depth - 1, visited)
                )

        # Reverse relations
        elif isinstance(field, (ManyToOneRel, ManyToManyRel)):
            related_model = field.related_model
            if isinstance(related_model, type) and issubclass(related_model, Model):
                nested_prefix = f"{prefix}{field.name}__"
                fields.extend(
                    get_string_fields(related_model, nested_prefix, depth - 1, visited)
                )

    return fields
