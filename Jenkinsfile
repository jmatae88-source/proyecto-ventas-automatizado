pipeline {
    agent any
    
    stages {
        stage('Limpieza Previa') {
            steps {
                echo 'Limpiando contenedores existentes...'
                bat 'docker rm -f db-ventas || echo "No existia contenedor previo"'
                echo 'Limpiando estado de Terraform...'
                dir('terraform') {
                    bat 'rmdir /s /q .terraform 2>nul || echo "No habia .terraform"'
                    bat 'del terraform.tfstate* 2>nul || echo "No habia state"'
                }
            }
        }
        
        stage('Infraestructura con Terraform') {
            steps {
                echo 'Levantando Base de Datos con Terraform...'
                dir('terraform') {
                    bat 'terraform init'
                    bat 'terraform apply -auto-approve'
                }
                echo 'Esperando a que PostgreSQL inicie (20 segundos)...'
                bat 'powershell -Command "Start-Sleep -Seconds 20"'
            }
        }
        
        stage('Procesamiento de Datos') {
            steps {
                echo 'Instalando dependencias...'
                bat 'pip install pandas psycopg2-binary'
                echo 'Ejecutando script de procesamiento...'
                bat 'python scripts/procesar_ventas.py'
            }
        }
        
        stage('Validación Final') {
            steps {
                echo 'Verificando datos en PostgreSQL...'
                bat 'docker exec db-ventas psql -U admin -d ventas_db -c "SELECT COUNT(*) FROM ventas;"'
                echo 'Pipeline finalizado exitosamente'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completado'
        }
        success {
            echo 'Pipeline exitoso'
        }
        failure {
            echo 'El pipeline fallo - revisar logs'
        }
    }
}