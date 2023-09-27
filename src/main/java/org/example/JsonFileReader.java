package org.example;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class JsonFileReader {
    public void ReadJsonFile() {
        // Create an ObjectMapper to parse JSON
        ObjectMapper objectMapper = new ObjectMapper();
        Functions functions = new Functions();

        try (BufferedReader br = new BufferedReader(new FileReader("company-stakeholders.json"))) {
            String line;
            while ((line = br.readLine()) != null) {
                // Parse each line as a JSON object
                try {
                    JsonNode jsonNode = objectMapper.readTree(line);

                    String name = jsonNode.get("first_name").asText();
                    String country = functions.getCountryFromIP(jsonNode);
                    String apiUrl = "https://api.genderize.io/?name=" + name + "&country_id=" + country;

                    String gender = functions.getGenderFromNameAndCountry(apiUrl);
                    System.out.println(gender);

                    //TODO: Create email!

                } catch (IOException e) {
                    System.err.println("Error parsing JSON: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }
}
