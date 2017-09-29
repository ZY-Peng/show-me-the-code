import java.util.Arrays;

/**
 * @Author: single-wolf
 * @Date: 2017/9/26 15:59
 * @Description: TODO
 */
public class BaseSort {
    public static final int INSERT_MIN = 5;

    public static void InsertSort(int[] num) {
        InsertSort(num, 0, num.length - 1);
    }

    public static void InsertSort(int[] num, int from, int to) {
        if (to - from > 1) {
            int tmp, i, j;
            for (i = from + 1; i <=to; i++) {
                if (num[i] < num[i - 1]) {
                    tmp = num[i];
                    for (j = i - 1; j >= from && tmp < num[j]; --j)
                        num[j + 1] = num[j];
                    num[j + 1] = tmp;
                }
            }
        }
    }

    public static void BInsertSort(int[] num) {
        BInsertSort(num, 0, num.length - 1);
    }

    public static void BInsertSort(int[] num, int from, int to) {
        if (to - from > 1) {
            int i, j, tmp, low, mid, high;
            for (i = from + 1; i <= to; i++) {
                tmp = num[i];
                low = 0;
                high = i - 1;
                while (low <= high) {
                    mid = (low + high) / 2;
                    if (tmp < num[mid]) high = mid - 1;
                    else low = mid + 1;
                }
                for (j = i - 1; j >= high + 1; --j)
                    num[j + 1] = num[j];
                num[j + 1] = tmp;
            }
        }
    }

    public static int[] ShellSort(int[] num) {
        int len = num.length;
        if (len > 1) {
            int i, j, tmp, k, gap;
            for (gap = len / 2; gap > 0; gap /= 2) {
                for (i = 0; i < gap; i++) {
                    for (j = i + gap; j < len; j += gap) {
                        if (num[j] < num[j - gap]) {
                            tmp = num[j];
                            for (k = j - gap; k >= 0 && tmp < num[k]; k -= gap)
                                num[k + gap] = num[k];
                            num[k + gap] = tmp;
                        }
                    }
                }
            }
        }
        return num;
    }

    public static int[] BubbleSort(int[] num) {
        int len = num.length;
        if (len > 1) {
            int i, j, tmp;
            boolean change = true;
            for (i = len - 1; i >= 1 && change; --i) {
                change = false;
                for (j = 0; j < i; j++) {
                    if (num[j] > num[j + 1]) {
                        swap(num, j, j + 1);
                        change = true;
                    }
                }
            }
        }
        return num;
    }

    private static int Partition(int[] num, int low, int high) {
        int tmp = num[low];
        while (low < high) {
            while (low < high && num[high] >= tmp) --high;
            num[low] = num[high];
            while (low < high && num[low] <= tmp) ++low;
            num[high] = num[low];
        }
        num[low] = tmp;
        return low;
    }

    public static void QuickSort(int[] num) {
        QuickSort(num, 0, num.length - 1);
    }

    public static void QuickSort(int[] num, int low, int high) {
        if (low < high) {
            int pivoloc = Partition(num, low, high);
            QuickSort(num, low, pivoloc - 1);
            QuickSort(num, pivoloc + 1, high);
        }
    }

    public static void Merge(int[] num, int[] other, int from, int mid, int to) {
        int i, j;
        if (num == other) {
            num = Arrays.copyOf(num, num.length);
        }
        for (i = mid + 1, j = from; from <= mid && i <= to; ++j) {
            if (num[from] <= num[i]) other[j] = num[from++];
            else other[j] = num[i++];
        }
        if (from <= mid) other[j++] = num[from];
        if (i <= to) other[j++] = num[i];
    }

    private static void Msort(int[] num, int[] other, int from, int to) {
        if (from == to) other[from] = num[to];
        else {
            int mid = (from + to) / 2;
            int[] tmp = new int[num.length];
            Msort(num, tmp, from, mid);
            Msort(num, tmp, mid + 1, to);
            Merge(tmp, other, from, mid, to);
        }
    }

    public static void MergeSort(int[] num) {
        Msort(num, num, 0, num.length - 1);
    }

    public static void MergeSortSubInsert(int[] num) {
        MergeSortSubInsert(num, 0, num.length - 1);
    }

    public static void MergeSortSubInsert(int[] num, int from, int to) {
        if (to - from > 1) {
            if (to - from < INSERT_MIN) {
                InsertSort(num, from, to);
            } else {
                int mid = (from + to) / 2;
                MergeSortSubInsert(num, from, mid);
                MergeSortSubInsert(num, mid + 1, to);
                Merge(num, num, from, mid, to);
            }
        }
    }

    public static int[] HeapSort(int num[]) {
        int len = num.length;
        if (len > 1) {
            int i;
            for (i = len / 2 - 1; i >= 0; --i)
                HeapAdjust(num, i, len - 1);
            for (i = len - 1; i > 0; --i) {
                swap(num, 0, i);
                HeapAdjust(num, 0, i - 1);
            }
        }
        return num;
    }

    private static void HeapAdjust(int num[], int from, int to) {
        int j, tmp;
        tmp = num[from];
        for (j = 2 * from + 1; j <= to; j = 2 * j + 1) {
            if (j < to && num[j] < num[j + 1]) ++j;
            if (tmp > num[j]) break;
            num[from] = num[j];
            from = j;
        }
        num[from] = tmp;
    }

    private static void swap(int[] nums, int one, int other) {
        int tmp = nums[one];
        nums[one] = nums[other];
        nums[other] = tmp;
    }

    private static void print(int[] nums) {
        System.out.print("[ ");
        for (int num : nums) {
            System.out.print(num + " ");
        }
        System.out.println("]");
    }

    public static void main(String[] args) {
        int[] nums1 = new int[]{2, 6, 4, 3, 9, 7, 0, 11, 5};
//        InsertSort(nums1);
//        BInsertSort(nums1);
//        BubbleSort(nums1);
//        ShellSort(nums1);
//        QuickSort(nums1);
//        HeapSort(nums1);
//        MergeSort(nums1);
        MergeSortSubInsert(nums1);
        print(nums1);
    }
}
