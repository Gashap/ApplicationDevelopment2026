namespace ApplicationDevelopment2026
{
	// LeetCode 1. Two Sum — https://leetcode.com/problems/two-sum/
	internal static class TwoSum
	{
		// a. «В лоб»: перебор всех пар.
		// Время O(n²), память O(1).
		// Отправка: https://leetcode.com/problems/two-sum/submissions/2171541053
		public static int[] BruteForce(int[] nums, int target)
		{
			for (int i = 0; i < nums.Length - 1; i++)
			{
				for (int j = i + 1; j < nums.Length; j++)
				{
					if (nums[i] + nums[j] == target)
					{
						return new[] { i, j };
					}
				}
			}

			return Array.Empty<int>();
		}

		// b. HashMap: значение → индекс, для текущего числа ищем (target − число).
		// Время O(n), память O(n).
		// Отправка: https://leetcode.com/problems/two-sum/submissions/2171543012
		public static int[] HashMap(int[] nums, int target)
		{
			var indexByValue = new Dictionary<int, int>();

			for (int i = 0; i < nums.Length; i++)
			{
				int complement = target - nums[i];
				if (indexByValue.TryGetValue(complement, out int j))
				{
					return new[] { j, i };
				}

				indexByValue[nums[i]] = i;
			}

			return Array.Empty<int>();
		}
	}
}
