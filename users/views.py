from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse_lazy
from django.views.generic import CreateView
from .forms import CreationForm

User = get_user_model()


#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def get_token(request):
#     """Получение JWT-токена"""
#     serializer = GetTokenSerializer(data=request.data)
#     if not serializer.is_valid():
#         raise ValidationError(serializer.errors)
#     user = get_object_or_404(
#         User,
#         email=serializer.validated_data['email'],
#         confirmation_code=serializer.validated_data['confirmation_code'])
#     refresh_tokens = RefreshToken.for_user(user)
#     tokens = {
#         'refresh': str(refresh_tokens),
#         'access': str(refresh_tokens.access_token),
#     }
#     return Response({'message': tokens.items()})
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def registration(request):
#     """Регистрация пользователя и получение confirmation_code"""
#     serializer = RegistrationSerializer(data=request.data)
#     if not serializer.is_valid():
#         raise ValidationError(serializer.errors)
#     email = serializer.validated_data['email']
#     username = serializer.validated_data['username']
#     if not email:
#         return Response(
#             {
#                 'message':
#                     {
#                         'Ошибка': 'Не указана почта для регистрации'
#                     }
#             },
#             status=status.HTTP_403_FORBIDDEN
#         )
#     token = PasswordResetTokenGenerator()
#     user = get_user_model()
#     user.email = email
#     user.last_login = timezone.now()
#     user.password = ''
#     confirmation_code = token.make_token(user)
#     try:
#         query_get, flag = get_user_model().objects.get_or_create(
#             email=email,
#             defaults={
#                 'username': username,
#                 'confirmation_code': confirmation_code,
#                 'last_login': timezone.now()})
#         if not flag:
#             return Response(
#                 {
#                     'message':
#                         {
#                             'Ошибка': ('Пользователь с таким email '
#                                        'уже существует.')
#                         }
#                 },
#                 status=status.HTTP_403_FORBIDDEN
#             )
#     except HTTPError:
#         return Response(
#             {
#                 'message':
#                     {
#                         'Ошибка': 'Ошибка запроса'
#                     }
#             },
#             status=status.HTTP_403_FORBIDDEN
#         )
#     send_mail(
#         'Подтверждение адреса электронной почты yamdb',
#         f'Вы получили это письмо, потому что регистрируетесь на ресурсе '
#         f'foodgram Код подтверждения confirmation_code = '
#         f'{confirmation_code}',
#         settings.DEFAULT_FROM_EMAIL,
#         [email, ],
#         fail_silently=False,
#     )
#     return Response(
#         {
#             'message':
#                 {
#                     'ОК': f'Пользователь c email {email} успешно создан. '
#                           'Код подтверждения отправлен на электронную почту'
#                 }
#         }
#     )
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-id', 'role')
#     serializer_class = UserSerializer
#     # permission_classes = [IsAuthenticated, IsAdmin]
#     lookup_field = 'username'
#
#     @action(
#         methods=['get', 'patch'],
#         detail=False,
#         # permission_classes=[IsAuthenticated],
#         url_path='me'
#     )
#     def me(self, request):
#         serializer = UserSerializer(request.user, many=False)
#         if request.method == 'PATCH':
#             serializer = UserSerializer(
#                 request.user, data=request.data, partial=True
#             )
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )
#

class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'reg.html'
