from .models import Catagory

def catagoryProcessor(request):
    catagories = Catagory.objects.all()
    return {"catagories" : catagories}