from django.contrib import admin
from weddings.models import (
    Person,
    PersonGroup,
    Photo,
    PhotoType,
    Wedding,
    Relationship,
    DonateBox,
    ImportantDay,
    LoveStory,
    Wish,
    PhotosZip,
    Invitation,
)

admin.site.register(Person)
admin.site.register(PersonGroup)
admin.site.register(Photo)
admin.site.register(PhotoType)
admin.site.register(Wedding)
admin.site.register(Relationship)
admin.site.register(DonateBox)
admin.site.register(ImportantDay)
admin.site.register(LoveStory)
admin.site.register(Wish)
admin.site.register(PhotosZip)
admin.site.register(Invitation)
