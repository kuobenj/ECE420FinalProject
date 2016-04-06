package com.statuskuo.ece420finalproject;

/**
 * Created by Status on 4/5/2016.
 */

import android.graphics.*;
import android.util.Log;

import org.bytedeco.javacpp.Loader;
import org.bytedeco.javacpp.opencv_core;
import org.bytedeco.javacv.Frame;
import org.bytedeco.javacv.OpenCVFrameConverter;

import static org.bytedeco.javacpp.opencv_core.*;
import static org.bytedeco.javacpp.opencv_imgproc.*;
import static org.bytedeco.javacpp.opencv_imgcodecs.*;

public class PreProcessor {
    public static void preprocess(String filename) {
        /********** Reading Input image **********/

        // Load an image from file - change this based on your image name
        IplImage pInpImg = cvLoadImage(filename);
        if (pInpImg == null) {
            Log.e("Image Error", "failed to load input image\n");
            return;
        }
        else {
            Log.d("Image Loading", "Image Loaded Successfully");
        }

        //Convert to mat
        Mat orig = cvarrToMat(pInpImg);  // default additional arguments: don't copy data.
        Mat output = orig;

        Log.d("Image Conversion", "Image Converted to Mat");

        /**********  Code for contour detection **********/
        //Convert to grayscale
        Mat gray = new Mat();
        cvtColor(orig, gray, CV_BGR2GRAY);

        Log.d("Image Conversion", "Image Converted to Gray");

        //Gaussian blur to remove noise
        GaussianBlur(gray, gray, new Size(5, 5), 0, 0, BORDER_DEFAULT);

        Log.d("Image Conversion", "Image Blurred");

        //Create threshold image
        Mat thresh = new Mat();
        adaptiveThreshold(gray, thresh, 255, 1, 1, 11, 2);

        Log.d("Image Conversion", "Image Thresholded");

        cvSaveImage(filename + "greyandthresh.jpg", new IplImage(thresh));

        Log.d("Image Conversion", "Thresholded image saved");

        /**********  Finding contours  **********/
//        vector<vector<Point> > contours;
//        vector<Vec4i> hierarchy;
//        findContours(thresh, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);

        CvSeq contour = new CvSeq(null);
        CvSeq contour2 = new CvSeq(null);
        CvSeq points = new CvSeq(null);
        CvMemStorage storage = CvMemStorage.create();
        cvFindContours(new IplImage(thresh), storage, contour, Loader.sizeof(CvContour.class),
                CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE);
        contour2 = contour;

        Log.d("Contours", "Contours Found");

        /**********  Finding largest countour **********/
        //cout << "# of contours dectected: " << contours.size() << endl;

//        double largest_area=100;
//        int largest_contour_index=0;
//        double peri = 0;
//        vector<Point> approxCurve;
//
//        Rect bounding_rect;
//        for( int i = 0; i< contours.size(); i++ ){
//            //Find the area of contour
//            double a=contourArea(contours[i],false);
//            if(a>largest_area){
//                largest_area=a;
//                //Store the index of largest contour
//                largest_contour_index=i;
//                approxPolyDP(contours[i], approxCurve, 0.05*arcLength(contours[i], true), true);
//                bounding_rect=boundingRect(contours[i]); // Find the bounding rectangle for biggest contour
//            }
//        }
        //cout << "Size of largest area: " << (double)largest_area << endl;
        double largest_area = 100;
        int largest_contour_index = 0;
        int i = 0;
        opencv_core.Rect bounding_rect;
        while (contour != null && !contour.isNull()) {
            if (contour.elem_size() > 0) {
                double a = cvContourArea(contour);
                if (a > largest_area) {
                    largest_area = a;
                    //Store the index of largest contour
                    largest_contour_index = i;
                    points = cvApproxPoly(contour, Loader.sizeof(CvContour.class),
                            storage, CV_POLY_APPROX_DP, cvContourPerimeter(contour) * 0.02, 0);
//                    bounding_rect = boundingRect(new Mat(points)); // Find the bounding rectangle for biggest contour
                    i++;
                }

//                cvDrawContours(grabbedImage, points, CvScalar.BLUE, CvScalar.BLUE, -1, 1, CV_AA);
            }
            contour = contour.h_next();
        }


        /**********  Constants for drawing  **********/
//        int thickness = 20;
//        Scalar color(128,128,255);
//        Scalar white(255,255,255);
//        Scalar red(0,0,255);
//        Scalar blue(255,0,0);
//        //cout << "Curve size: " << approxCurve.size() << endl;

        /**********  Draw around contour (Testing only)  **********/
        // for(int i = 0; i < approxCurve.size(); i++){
        //   line(orig, approxCurve.at(i%approxCurve.size()), approxCurve.at((i+1)%approxCurve.size()), blue, thickness);
        // }


        /**********  Draw around largest rectangle **********/
//        Mat dst = thresh;
//
//        // Draw the largest contour using previously stored index.
//        drawContours(dst, contours,largest_contour_index, color, CV_FILLED, 8, hierarchy);
//        vector<Point> largestrect(4);
//        if (approxCurve.size() >= 4 && (approxCurve.size() <= 10)){
//            largestrect = findLargestQuad(approxCurve);
//        }
//
//        if(!largestrect.empty()){
//            //cout << "Largest Rect Size: " << (double)contourArea(largestrect,false) << endl;
//            for(int i = 0; i < largestrect.size(); i ++){
//                //line(orig, approxCurve.at(i%approxCurve.size()), approxCurve.at((i+1)%approxCurve.size()), red, thickness);
//                line(orig, largestrect.at(i%largestrect.size()), largestrect.at((i+1)%largestrect.size()), red, thickness);
//            }
//        }
//        else{
//            cout << "No suitable rectangle detected" << endl;
//        }

        //Bounding rectangle (For testing)
        //rectangle(orig, bounding_rect,  white, thickness, 8,0);

//        output = orig;

        IplImage dst = new IplImage(thresh);

//        i = 0;
        // Draw the largest contour using previously stored index.
//        while (contour != null && !contour.isNull()) {
//            if (contour.elem_size() > 0) {
//                if (i == largest_contour_index) {
        cvDrawContours(dst, points, CvScalar.RED, CvScalar.RED, -1, 1, CV_AA);
//                }
//                i++;
//            }
//            contour = contour.h_next();
//        }

//        CvSeq largestrect = new CvSeq(null);
//        if ((points.elem_size()) >= 4 && (points.elem_size() <= 10)){
//            largestrect = findLargestQuad(points);
//        }
//
//        if(largestrect.elem_size() > 0){
//            //cout << "Largest Rect Size: " << (double)contourArea(largestrect,false) << endl;
//            for(i = 0; i < largestrect.elem_size(); i ++){
//                //line(orig, approxCurve.at(i%approxCurve.size()), approxCurve.at((i+1)%approxCurve.size()), red, thickness);
//                cvLine();line(orig, largestrect.at(i%largestrect.size()), largestrect.at((i+1)%largestrect.size()), red, thickness);
//            }
//        }
//        else{
//            cout << "No suitable rectangle detected" << endl;
//        }
//
//        //Bounding rectangle (For testing)
//        //rectangle(orig, bounding_rect,  white, thickness, 8,0);
//
//        output = orig;


        /**********  Writing output image **********/
        // using a different image format -- .png
//        if(!imwrite(argv[2], output)){
//            fprintf(stderr, "failed to write image file\n");
//        }
        cvSaveImage(filename + "processed.jpg", dst);


        /**********  Freeing Memory **********/
        cvReleaseImage(pInpImg);
        return;

    }
    /**********  HELPER FUNCTIONS **********/

    /**
     * findLargestQuad(vector<Point> input)
     * Inputs: vector of points for a Curve
     * Output: vector of 4 points
     * Description: given an input vector of points, returns a vector with 4 points
     * 					that form the largest rectangular area within those points.
     * 					If the input vector is less than 4 points, return empty vector.
     */
//    public static CvSeq findLargestQuad(CvSeq cvSeq){
//        vector<Point> output(4);
//        vector<Point> temp(4);
//        float largest_area = 0;
//
//        if(input.size() < 4){
//            return vector<Point>();
//        }
//
//        for(int a = 0; a < input.size(); a++){
//            for(int b = 0; b < input.size(); b++){
//                for(int c = 0; c < input.size(); c++){
//                    for(int d = 0; d < input.size(); d++){
//                        temp.clear();
//                        temp.push_back(input[a]);
//                        temp.push_back(input[b]);
//                        temp.push_back(input[c]);
//                        temp.push_back(input[d]);
//                        if(a != b && a != c && a != d && b != c && b != d && c != d){
//                            float area = contourArea(temp,false);
//                            if(area > largest_area){
//                                output.clear();
//                                largest_area = area;
//                                output = temp;
//                            }
//                        }
//                    }
//                }
//            }
//        }
//        //cout << "Largest from findLargestQuad: " << largest_area <<endl;
//        return output;
//    }
}
