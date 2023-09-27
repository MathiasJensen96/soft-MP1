package org.example;

import com.fasterxml.jackson.databind.JsonNode;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.ProtocolException;
import java.net.URL;

public class Functions {
    public String getCountryFromIP(JsonNode jsonNode) throws IOException {
        String curlStart = "curl \"ipinfo.io/";
        String IP = jsonNode.get("ip_address").asText();
        String curlEnd = "/country?token=f7bf654f6196a8\"";
        String curlCommand = curlStart + IP + curlEnd;
        StringBuilder country = new StringBuilder();

        try {
            ProcessBuilder processBuilder = new ProcessBuilder("/bin/bash", "-c", curlCommand);
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();

            // Read the output of the command
            InputStream inputStream = process.getInputStream();
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            BufferedReader reader = new BufferedReader(inputStreamReader);
            StringBuilder result = new StringBuilder();

            String line;
            while ((line = reader.readLine()) != null) {
                result.append(line).append("\n");
            }

            // Wait for the process to finish
            int exitCode = process.waitFor();

            if (exitCode == 0) {
                country.append(result.charAt(result.length()-3));
                country.append(result.charAt(result.length()-2));
            } else {
                System.out.println("Curl command failed with exit code: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        return country.toString();
    }

    public String getGenderFromNameAndCountry(String apiUrl) throws IOException {

        URL url = new URL(apiUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");

        // Get the response
        BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }

        in.close();
        connection.disconnect();

        return response.toString();

    }
}

