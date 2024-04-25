from rest_framework import views
from ecommerce_web_app.helpers import custom_response
from rest_framework.permissions import AllowAny
import cloudinary
from .models import Photo
from .serializers import PhotoSerializer


class PhotoAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            photos = Photo.objects.all()
            serializers = PhotoSerializer(photos, many=True)
            return custom_response(
                "Get all photos successfully!", "Success", serializers.data, 200
            )
        except Exception as e:
            return custom_response("Get all photos failed!", "Error", str(e), 400)

    def post(self, request):
        if "uploadImages" not in request.FILES:
            return custom_response(
                "No upload resource", "Error", "No image file found in request", 400
            )

        if request.method == "POST":
            images = request.FILES.getlist("uploadImages")
            data = []
            for image in images:
                try:
                    upload_result = cloudinary.uploader.upload(image)
                    img_obj = Photo(
                        id=upload_result["public_id"],
                        url=upload_result["secure_url"],
                        filename=upload_result["original_filename"],
                        format=upload_result["format"],
                        width=upload_result["width"],
                        height=upload_result["height"],
                        created_at=upload_result["created_at"],
                    )
                    img_obj.save()
                    serializer = PhotoSerializer(img_obj)
                    data.append(serializer.data)
                except Exception as e:
                    return custom_response(
                        "Upload images failed!", "Error", str(e), 400
                    )

            return custom_response("Upload images successfully!", "Success", data, 200)

    def put(self, request, photo_id):
        try:
            photo = Photo.objects.get(id=photo_id)
            serializer = PhotoSerializer(photo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return custom_response(
                    "Update photo successfully!", "Success", serializer.data, 200
                )
            else:
                return custom_response(
                    "Invalid data provided for update!", "Error", serializer.errors, 400
                )
        except Photo.DoesNotExist:
            return custom_response(
                "Photo not found!",
                "Error",
                "Photo with provided ID does not exist",
                404,
            )
        except Exception as e:
            return custom_response("Update photo failed!", "Error", str(e), 400)

    def delete(self, request, photo_id):
        try:
            photo = Photo.objects.get(id=photo_id)
            photo.delete()
            return custom_response("Delete photo successfully!", "Success", None, 204)
        except Photo.DoesNotExist:
            return custom_response(
                "Photo not found!",
                "Error",
                "Photo with provided ID does not exist",
                404,
            )
        except Exception as e:
            return custom_response("Delete photo failed!", "Error", str(e), 400)
