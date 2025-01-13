import os
import shutil
import subprocess

def handle_remove_readonly(func, path, exc_info):
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_git_repos(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirnames:
            git_dir = os.path.join(dirpath, '.git')
            print(f'Removendo {git_dir}')
            shutil.rmtree(git_dir, onerror=handle_remove_readonly)

def init_new_repo(root_dir):
    os.chdir(root_dir)
    subprocess.run(['git', 'init'])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Initial commit'])

def push_to_remote(root_dir, remote_url):
    os.chdir(root_dir)
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url])
    subprocess.run(['git', 'push', '-u', 'origin', 'master'])

if __name__ == "__main__":
    root_dir = 'F:/projetos'
    remote_url = 'https://github.com/Caboginho/Projetos.git'
    
    remove_git_repos(root_dir)
    init_new_repo(root_dir)
    push_to_remote(root_dir, remote_url)
    
    print('Repositorios Git removidos, novo repositório inicializado e arquivos enviados para o repositório remoto.')
