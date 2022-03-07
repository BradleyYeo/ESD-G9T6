FROM openjdk:17-jdk
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} login-0.0.1-SNAPSHOT.jar 
ENTRYPOINT ["java","-jar","/login-0.0.1-SNAPSHOT.jar"]
