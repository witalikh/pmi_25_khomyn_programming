from rest_framework import status, filters

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .serializers import CertificateSerializer
from .models import Certificate


class FirstCertificateAPIView(ListAPIView):
    """
    (List)APIView class for "GET" and "POST" methods
    from url /api/container/
    "GET" is auto-defined (with filters and ordering) for getting certificates
    """

    # queryset and serializer for "GET" auto-define
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

    http_method_names = ["get", "post"]

    # custom filters
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["date_of_birth", "end_date", "id",
                     "international_passport", "start_date", "username", "vaccine"]

    def post(self, request):
        """
        "POST" HTTP-request, append database with new certificate
        """
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200,
                             "message": "Certificate successfully created",
                             "certificate": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SecondCertificateAPIView(APIView):
    """
    APIView class for "PUT", "GET" and "DELETE" requests
    from url /api/container/<some id to perform action with>
    """
    def get_object(self, identifier):
        """
        Helper method, looking for certificate with some id
        """
        try:
            return Certificate.objects.get(id=identifier)
        except Certificate.DoesNotExist:
            return Response({"status": 404,
                             "message": "Certificate not found"},
                            status=status.HTTP_404_NOT_FOUND)

    def get(self, request, identifier):
        """
        "GET" HTTP-request, obtain certificate by id
        """
        certificate = self.get_object(identifier)
        if isinstance(certificate, Response):
            return certificate

        serializer = CertificateSerializer(certificate)
        return Response(serializer.data)

    def put(self, request, identifier):
        """
        "PUT" HTTP-request, edit the existing record (by id)
        """

        certificate = self.get_object(identifier)
        if isinstance(certificate, Response):
            return certificate

        certificate_data = JSONParser().parse(request)
        serializer = CertificateSerializer(certificate, data=certificate_data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200,
                             "message": "Certificate successfully updated",
                             "certificate": serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"status": 400,
                         "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, identifier):
        """
        "DELETE" HTTP-request, delete certificate by id
        """
        certificate = self.get_object(identifier)
        if isinstance(certificate, Response):
            return certificate

        certificate.delete()
        return Response({"status": 200,
                         "message": "Successfully deleted!"},
                        status=status.HTTP_200_OK)
