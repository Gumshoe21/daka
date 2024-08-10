package main

import (
	"encoding/json"
	"io"
	"os"

	tea "github.com/charmbracelet/bubbletea"
)

func (m model) Init() tea.Cmd {
	return nil
}

type view struct {
	name        string
	cursorLimit int
}

type model struct {
	views       []view
	cursor      int
	cursorLimit int
	selected    map[int]struct{}
}

type timer struct {
	Name       string `json:"name"`
	Session    int    `json:"session"`
	ShortBreak int    `json:"shortBreak"`
	LongBreak  int    `json:"longBreak"`
}

type Config struct {
	timers []timer `json:"timers"`
}

func getAllTimers(configPath string) ([]timer, error) {
	config, err := loadConfig("timers.json")
	if err != nil {
		return nil, nil
	}
	return config.timers, nil
}

func loadConfig(configPath string) (*Config, error) {
	configFile, err := os.Open(configPath)
	if err != nil {
		return nil, nil
	}

	byteValue, err := io.ReadAll(configFile)
	if err != nil {
		return nil, nil
	}

	var config Config
	if err := json.Unmarshal(byteValue, &config); err != nil {
		return nil, nil
	}

	return &config, nil
}

func initializeModel() model {
	m := model{
		views: []view{
			{name: "Main Menu", cursorLimit: 3},
			{name: "View Timers", cursorLimit: 3},
		},
		selected: make(map[int]struct{}),
	}
	m.cursorLimit = m.views[0].cursorLimit
	return m
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	panic("func not implemented")
}

func (m model) View() string {
	panic("func not implemented")
}
