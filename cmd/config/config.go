package config

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

type Timer struct {
	Name       string `json:name`
	Countdown  int    `json:countdown`
	ShortBreak int    `json:shortBreak`
	LongBreak  int    `json:longBreak`
}

type Config struct {
	Timers []Timer `json:timers`
}

func LoadConfig(file string) (*Config, error) {
	// open config file
	configFile, err := os.Open(file)
	if err != nil {
		return nil, fmt.Errorf("Could not open config file: %w", err)
	}
	defer configFile.Close()

	// read config file
	byteValue, err := ioutil.ReadAll(configFile)
	if err != nil {
		return nil, fmt.Errorf("Could not read config file: %w", err)
	}

	// parse the read config file and store it in 'config'
	var config Config
	if err := json.Unmarshal(byteValue, &config); err != nil {
		return nil, fmt.Errorf("Could not unmarshal config: %w", err)
	}

	return &config, nil
}
