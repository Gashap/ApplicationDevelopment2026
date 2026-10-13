namespace ApplicationDevelopment2026
{
	public class Solution
	{
		public int[] TwoSum_A(int[] nums, int target)
		{
			for (int i = 0; i < nums.Length; i++)
			{
				for (int j = i + 1; j < nums.Length; j++)
				{
					if (nums[i] + nums[j] == target)
					{
						return [i, j];
					}
				}
			}

			return [];
		}

		public int[] TwoSum_B(int[] nums, int target)
		{
			var dict = new Dictionary<int, int>();
			for (int i = 0; i < nums.Length; i++)
			{
				int complement = target - nums[i];

				if (dict.TryGetValue(complement, out int value))
				{
					return [value, i];
				}

				dict[nums[i]] = i;
			}

			return [];
		}
	}
}
