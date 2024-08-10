package main

import (
	"fmt"
	"io/ioutil"
	"log"

	"github.com/gumshoe21/daka/cmd/config"
)

func main() {
	timers := config.InitializeTimers()
	// p := tea.NewProgram(initializeModel())
	// if _, err := p.Run(); err != nil {
	// 	fmt.Printf("Alas, there's been an error: %v", err)
	// 	os.Exit(1)
	// }
	// Load the JSON data from file
	_, err := ioutil.ReadFile("timers.json")
	if err != nil {
		log.Fatal(err)
	}

	// Unmarshal the JSON data into a slice of timer structs
	// var timers []timer
	// err = json.Unmarshal(data, &timers)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// Example usage of AddTimer function
	newTimer := config.Timer{
		Name:       "New Timer",
		Session:    40,
		ShortBreak: 8,
		LongBreak:  20,
	}

	config.AddTimer("timers.json", newTimer)
	if err != nil {
		log.Fatal(err)
	}
	// Print the loaded timers
	for _, t := range timers {
		fmt.Printf("Name: %s, Session: %d, ShortBreak: %d, LongBreak: %d\n",
			t.Name, t.Session, t.ShortBreak, t.LongBreak)
	}
}
