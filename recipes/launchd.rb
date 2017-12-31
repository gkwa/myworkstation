directory '/usr/local/bin' do
  recursive true
end

file '/usr/local/bin/brew_upgrade.sh' do
  content <<-EOH
     #!/bin/sh
     brew upgrade
     EOH
  mode '0755'
end

launchd 'homebrew.upgrade' do
  program '/usr/local/bin/brew_upgrade.sh'
  # start_calendar_interval 'Day' => '*', 'Hour' => 11
  # start_calendar_interval 'Weekday' => '7', 'Hourly' => 10
  # start_calendar_interval 'Weekday' => "1-7", "Hourly" => 10
  time_out 300
end
