package com.statuskuo.ece420finalproject;

/**
 * Created by Status on 4/4/2016.
 */

import static org.bytedeco.javacpp.opencv_core.*;
import static org.bytedeco.javacpp.opencv_imgproc.*;
import static org.bytedeco.javacpp.opencv_imgcodecs.*;

public class Smoother {
    public static void smooth(String filename) {
        IplImage image = cvLoadImage(filename);
        if (image != null) {
            cvSmooth(image, image, CV_MEDIAN, 3, 0, 0, 0);
            cvSaveImage(filename+"smoothed.jpg", image);
            cvReleaseImage(image);
        }
    }
}
