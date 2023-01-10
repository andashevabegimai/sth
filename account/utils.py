from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    message = f'congratulations! вы зарегались на нашем сайте. активируйте аккаунт отправив нам этот код ' \
              f'{activation_code}'
    send_mail('активация аккаунта', message, 'test@gmail.com', [email])
