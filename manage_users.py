from app import app, db
from app.models.user import User

def make_admin():
    with app.app_context():
        username = input("Digite o nome de usuário que você deseja tornar administrador: ")
        user = User.query.filter_by(username=username).first()
        if user:
            user.role = 'admin'
            db.session.commit()
            print(f"O usuário {username} agora é um administrador.")
        else:
            print(f"Usuário {username} não encontrado.")

if __name__ == '__main__':
    make_admin()
