FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN mvn package -q -DskipTests
RUN mkdir /build/ROOT && cd /build/ROOT && jar -xf /build/target/XXEReader-1.0.war

FROM tomcat:10.1-jdk17
RUN rm -rf /usr/local/tomcat/webapps/ROOT /usr/local/tomcat/logs /usr/local/tomcat/work /usr/local/tomcat/temp && \
    ln -s /tmp /usr/local/tomcat/logs && \
    ln -s /tmp /usr/local/tomcat/work && \
    ln -s /tmp /usr/local/tomcat/temp
COPY --from=build /build/ROOT /usr/local/tomcat/webapps/ROOT
ENV FLAG="CTF{placeholder}"
EXPOSE 8080
CMD ["sh", "-c", "echo \"$FLAG\" > /tmp/flag.txt && catalina.sh run"]
