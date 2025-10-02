#!/usr/bin/env python3
"""
Tests for Async/Await chapter.
Learn Python with Tests - Asynchronous Programming
"""

import pytest
import asyncio
from async_operations import AsyncOperations


class TestBasicAsync:
    """Test basic async/await functionality."""
    
    @pytest.mark.asyncio
    async def test_simple_async_function(self):
        """Should return value from async function."""
        async_ops = AsyncOperations()
        result = await async_ops.simple_async_function()
        assert result == "Hello, async world!"
    
    @pytest.mark.asyncio
    async def test_async_sleep_and_return(self):
        """Should sleep then return value."""
        async_ops = AsyncOperations()
        result = await async_ops.async_sleep_and_return(0.1, "test_value")
        assert result == "test_value"


class TestConcurrentOperations:
    """Test concurrent async operations."""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """Should simulate fetching data."""
        async_ops = AsyncOperations()
        result = await async_ops.fetch_data("https://api.example.com/data")
        assert "data" in result
        assert result["url"] == "https://api.example.com/data"
    
    @pytest.mark.asyncio
    async def test_fetch_multiple_urls(self):
        """Should fetch multiple URLs concurrently."""
        async_ops = AsyncOperations()
        urls = [
            "https://api.example1.com",
            "https://api.example2.com",
            "https://api.example3.com"
        ]
        results = await async_ops.fetch_multiple_urls(urls)
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["url"] == urls[i]


class TestProducerConsumer:
    """Test producer-consumer pattern."""
    
    @pytest.mark.asyncio
    async def test_producer_consumer(self):
        """Should implement producer-consumer pattern."""
        async_ops = AsyncOperations()
        queue = asyncio.Queue()
        items = ["item1", "item2", "item3"]
        
        # Run producer and consumer concurrently
        producer_task = asyncio.create_task(
            async_ops.producer(queue, items)
        )
        consumer_task = asyncio.create_task(
            async_ops.consumer(queue, len(items))
        )
        
        await producer_task
        consumed_items = await consumer_task
        
        assert consumed_items == items


class TestAsyncFileOperations:
    """Test asynchronous file operations."""
    
    @pytest.mark.asyncio
    async def test_write_and_read_file(self):
        """Should write and read file asynchronously."""
        async_ops = AsyncOperations()
        filename = "test_async_file.txt"
        content = "Hello, async file operations!"
        
        # Write file
        await async_ops.write_file_async(filename, content)
        
        # Read file
        read_content = await async_ops.read_file_async(filename)
        assert read_content == content
        
        # Cleanup
        import os
        if os.path.exists(filename):
            os.remove(filename)


class TestAsyncErrorHandling:
    """Test error handling in async operations."""
    
    @pytest.mark.asyncio
    async def test_async_timeout(self):
        """Should handle timeout in async operations."""
        async_ops = AsyncOperations()
        
        async def slow_operation():
            await asyncio.sleep(1.0)
            return "completed"
        
        with pytest.raises(asyncio.TimeoutError):
            await async_ops.async_with_timeout(slow_operation(), 0.1)
    
    @pytest.mark.asyncio
    async def test_semaphore_limiting(self):
        """Should limit concurrent operations with semaphore."""
        async_ops = AsyncOperations()
        semaphore = asyncio.Semaphore(2)  # Allow only 2 concurrent operations
        
        async def dummy_operation():
            await asyncio.sleep(0.1)
            return "done"
        
        # This should work within semaphore limit
        result = await async_ops.async_with_semaphore(semaphore, dummy_operation())
        assert result == "done"


if __name__ == '__main__':
    pytest.main([__file__])
