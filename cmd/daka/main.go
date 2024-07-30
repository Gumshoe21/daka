package main

import (
	"fmt"
	"log"
	"os"
	"reflect"
	"time"
)

type Message struct {
	Name string
	Body string
	Time int64
}

type Config struct{}

func ReadFile(filename string) ([]byte, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("error reading file: %w", err)
	}
	return data, nil
}

func OpenFile(filename string) (*os.File, error) {
	// Try to open the file for writing. If it doesn't exist, create it.
	file, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY, 0o644)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	return file, nil
}

func reflectStruct(m Message, file *os.File) {
	val := reflect.ValueOf(m)
	for i := 0; i < val.NumField(); i++ {
		field := val.Type().Field(i)
		value := val.Field(i)
		// Print the type and value to debug
		fmt.Printf("Field Name: %s, Type: %s, Value: %v\n", field.Name, value.Type(), value.Interface())

		// Use value.Interface() to get the concrete value
		_, err := fmt.Fprintf(file, "%s: %v\n", field.Name, value.Interface())
		if err != nil {
			fmt.Println("Error writing to file:", err)
			return
		}
	}
}

func main() {
	// Read the content of the file
	data, err := ReadFile("test.txt")
	if err != nil {
		log.Fatalf("Error reading file: %v", err)
	}
	fmt.Println("Read data:", string(data))

	// Create an instance of Message
	m := Message{"Matthew", "This is my message.", time.Now().UnixNano()}

	// OpenFile for writing
	file, err := OpenFile("test.txt")
	if err != nil {
		log.Fatalf("Could not open file: %v", err)
	}
	defer file.Close()

	// Write struct to file
	reflectStruct(m, file)
	fmt.Println("Data written to test.txt successfully.")
}
