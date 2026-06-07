pipeline {
    agent any
    
    stages {
        stage('Infraestructura con Terraform') {
            steps {
                echo 'Levantando Base de Datos con Terraform...'
                dir('terraform') {
                    bat 'terraform init'
                    bat 'terraform apply -auto-approve'
                }
                echo 'Esperando a que PostgreSQL inicie...'
                bat 'timeout /t 15 /nobreak'
            }
        }
        
        stage('Procesamiento de Datos') {
            steps {
                echo 'Instalando dependencias y ejecutando script...'
                bat 'pip install pandas psycopg2-binary'
                bat 'python scripts/procesar_ventas.py'
            }
        }
        
        stage('Validación Final') {
            steps {
                echo 'Pipeline finalizado exitosamente'
            }
        }
    }
}