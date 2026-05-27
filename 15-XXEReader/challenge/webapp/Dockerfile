FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN mvn package -q -DskipTests

FROM tomcat:10.1-jdk17
RUN rm -rf /usr/local/tomcat/webapps/ROOT
COPY --from=build /build/target/XXEReader-1.0.war /usr/local/tomcat/webapps/ROOT.war
RUN echo "FCTF{xxe_r34ds_y0ur_f1l3s}" > /app/flag.txt
EXPOSE 8080
CMD ["catalina.sh","run"]
