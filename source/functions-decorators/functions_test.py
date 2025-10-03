import time
from functions import timer, retry

def test_timer_decorator():
    @timer
    def slow_function():
        time.sleep(0.1)
        return "done"
    
    result = slow_function()
    assert result == "done"

def test_retry_decorator():
    call_count = 0
    
    @retry(max_attempts=3)
    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("Temporary failure")
        return "success"
    
    result = flaky_function()
    assert result == "success"
    assert call_count == 3