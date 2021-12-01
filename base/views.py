from django.core.paginator import Paginator

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.models import Branches
from base.serializers import BranchSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class BanksListAPI(generics.GenericAPIView):
    """
    List all the banks with respect to query params:

    query params: ifsc code
    response: bank details with branches
    """
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ifsc_code = request.GET.get('ifsc_code', None)
        if not ifsc_code:
            return Response({'message': 'Please provide ifsc code', 'status': 400})
        try:
            bank_details = Branches.objects.get(ifsc=ifsc_code)
        except Branches.DoesNotExist:
            return Response({'message': 'Bank with the IFSC code does not exist', 'status': 400})
        bank_data = BranchSerializer(bank_details)
        return Response({'message': 'Successfully fetched bank details', 'status': 200, 'data': bank_data.data})


class BranchesListAPI(generics.GenericAPIView):
    """
    List all the branches with respect to query params:

    query params: bank name and city name
    response: branch details with bank name
    """
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_size = int(request.GET.get('page_size', 10))
        page_number = int(request.GET.get('page_number', 1))
        city_name = request.GET.get('city_name', None)
        bank_name = request.GET.get('bank_name', None)
        if not (bank_name and city_name):
            return Response({'message': 'Please provide bank name and city name', 'status': 400})
        try:
            branches = Branches.objects.filter(city=city_name, bank__name=bank_name)
        except Branches.DoesNotExist:
            return Response({'message': 'Branch with the city name and bank name does not exist', 'status': 400})
        paginator = Paginator(branches, page_size)
        branches = paginator.page(page_number)
        branch_data = BranchSerializer(branches, many=True)
        return Response({'message': 'Successfully fetched branch details', 'status': 200, 'count': paginator.count,
                         'data': branch_data.data})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        If you want to add data outside token
         """

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializer(self.user)

        for key, value in serializer.data.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
