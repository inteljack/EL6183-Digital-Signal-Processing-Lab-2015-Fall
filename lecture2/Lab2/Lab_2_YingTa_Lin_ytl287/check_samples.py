#check_samples.py module function check
def check(sample,gain):
    limit = 0.0
    limit = 32767.0 / gain
    if abs(sample) > limit:
    	print sample,'exceed limit'
        sample = sample / abs(sample) * limit
    else:
        pass
    return sample
