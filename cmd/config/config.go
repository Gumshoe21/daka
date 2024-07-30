package config

type Timer struct {
	Name       string `json:name`
	Countdown  int    `json:countdown`
	ShortBreak int    `json:shortBreak`
	LongBreak  int    `json:longBreak`
}

type Config struct {
	Timers Timer[] `json:timers`
}
