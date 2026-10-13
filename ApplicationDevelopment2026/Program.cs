namespace ApplicationDevelopment2026
{
	internal class Program
	{
		static void Main(string[] args)
		{
			Human();
			Robot();
		}

		static void Human()
		{
			var solution = new Solution();

			var result = solution.TwoSum_A([2, 7, 11, 15], 9);
			Console.WriteLine($"{result[0]}, {result[1]}");

			result = solution.TwoSum_B([2, 7, 11, 15], 9);
			Console.WriteLine($"{result[0]}, {result[1]}");
		}

		static void Robot()
		{
			(int[] nums, int target)[] cases =
				{
				(new[] { 2, 7, 11, 15 }, 9),
				(new[] { 3, 2, 4 }, 6),
				(new[] { 3, 3 }, 6),
			};

			foreach (var (nums, target) in cases)
			{
				Console.WriteLine($"nums = [{string.Join(",", nums)}], target = {target}");
				Console.WriteLine($"  BruteForce: [{string.Join(",", TwoSum.BruteForce(nums, target))}]");
				Console.WriteLine($"  HashMap:    [{string.Join(",", TwoSum.HashMap(nums, target))}]");
			}
		}
	}
}
