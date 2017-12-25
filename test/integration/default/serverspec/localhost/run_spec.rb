require 'spec_helper'

describe command('lsof') do
  its(:exit_status) { should eq 0 }
end
