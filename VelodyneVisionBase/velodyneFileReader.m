%velodyneFileReader Creates a Velodyne PCAP file reader object.
%
%   veloReader = velodyneFileReader(filename, deviceModel) constructs a Velodyne
%   file reader object, veloReader, that can read in point cloud data from
%   a Velodyne PCAP file. filename is a character vector or a string specifying
%   the name of the Velodyne PCAP file. deviceModel is a character vector
%   or a string representing Velodyne Lidar model. Possible values for
%   deviceModel are 'VLP16', 'VLP32C', 'HDL32E' and 'HDL64E' for VLP-16,
%   VLP-32C, HDL-32E and HDL-64E device models respectively.
%
%   veloReader = velodyneFileReader(..., Name, Value) specifies
%   additional name-value pair arguments described below:
%
%   'CalibrationFile'  Name of an xml file containing Velodyne Lidar
%                      laser calibration data. If no calibration file is
%                      specified, a default calibration file with data
%                      obtained from Velodyne device manuals is chosen.
%
%                      Default: ''
%
%                      Note: Not providing a calibration file can lead to
%                      inaccurate results.
%
%   velodyneFileReader properties:
%      CurrentTime          - Time of the current point cloud measured from
%                             StartTime in seconds
%      FileName             - Name of the Velodyne PCAP file (read only)
%      DeviceModel          - Device model specified as a character vector
%                             or string (read only)
%      CalibrationFile      - Name of the Velodyne calibration xml file (read only)
%      NumberOfFrames       - Number of point cloud frames in the file (read only)
%      Duration             - Total duration of the file in seconds (read only)
%      StartTime            - Time of first point cloud in seconds (read only)
%      EndTime              - Time of last point cloud in seconds (read only)
%
%   velodyneFileReader methods:
%      readFrame            - Read a point cloud frame from file
%      hasFrame             - Determine if another point cloud is available
%      reset                - Reset to the beginning of the file
%
%   Notes
%   -----
%   - Providing incorrect device model for a given Velodyne PCAP file
%     shall not result in error, rather an improperly calibrated point
%     cloud will be generated.
%   - StartTime and EndTime are reported from top of the hour of file
%     recording and are not absolute times. For instance, if the file is
%     recorded for 7 minutes from 1:58 PM to 2:05 PM, then StartTime would
%     be 58*60 i.e. 3480 seconds and EndTime would be StartTime + 7*60 i.e.
%     3900 seconds.
%
%   Example : Read and visualize point clouds from Velodyne PCAP file.
%   ------------------------------------------------------------------
%   % Construct velodyneFileReader object.
%   veloReader = velodyneFileReader('lidarData_ConstructionRoad.pcap', 'HDL32E');
%
%   % Define X, Y, Z-axes limits, for pcplayer, in meters(m).
%   xlimits = [-60 60];
%   ylimits = [-60 60];
%   zlimits = [-20 20];
%
%   % Create the point cloud player.
%   player = pcplayer(xlimits, ylimits, zlimits);
%   % Set labels for pcplayer axes.
%   xlabel(player.Axes, 'X (m)');
%   ylabel(player.Axes, 'Y (m)');
%   zlabel(player.Axes, 'Z (m)');
%
%   % Specify that point cloud reading should start at 0.3 seconds from
%   % the beginning of file.
%   veloReader.CurrentTime = veloReader.StartTime + seconds(0.3);
%
%   % Display stream of point clouds until point clouds are not available.
%   while(hasFrame(veloReader) && player.isOpen())
%       ptCloudObj = readFrame(veloReader);
%       view(player, ptCloudObj.Location, ptCloudObj.Intensity);
%       pause(0.1);
%   end
%
%   See also velodyneFileReader/readFrame, velodyneFileReader/hasFrame,
%            pcread, pcplayer, pointcloud, pcshow.
%

% Copyright 2017-2018 MathWorks, Inc.

classdef velodyneFileReader < handle & matlab.mixin.SetGet & matlab.mixin.Copyable & ...
        vision.internal.EnforceScalarHandle
    
    properties (GetAccess = 'public', SetAccess = 'private')
        
        %FileName Name of the Velodyne PCAP file to read Velodyne Lidar data.
        FileName;
        
        %DeviceModel Velodyne Lidar device model.
        DeviceModel;
        
        %CalibrationFile Name of the XML file containing Velodyne laser
        %   lidar calibration data.
        CalibrationFile;
        
        %NumberOfFrames Total number of point clouds in the file.
        NumberOfFrames;
        
        %Duration Total length of the file in seconds represented as
        %   duration object.
        Duration;
        
        %StartTime Time of first point cloud in the file in seconds,
        %   represented as duration object. It is reported from the top of
        %   the hour of file recording.
        StartTime;
        
        %EndTime Time of last point cloud in the file in seconds,
        %   represented as duration object. It is reported from the top of
        %   the hour of file recording.
        EndTime;
    end
    
    properties (GetAccess = 'public', SetAccess = 'public', Dependent)
        
        %CurrentTime Time of the current point cloud being read in
        %   seconds from the StartTime. It ranges between StartTime
        %   and EndTime.
        CurrentTime;
    end
    
    properties (Access = 'private', Hidden)
        
        %LaserCalibrationData Laser calibration data loaded from xml file.
        LaserCalibrationData;
        
        %UserCurrentTimeFlag Flag to determine if CurrentTime property
        %   is set by user.
        UserCurrentTimeFlag;
        
        %CurrentTimeInternal Same as CurrentTime but used for internal
        %   purpose.
        CurrentTimeInternal;
        
        %Version Version Number used for backward compatibility.
        Version = 1.0;
    end
    
    properties (Access = 'private', Transient)
        
        %VelodyneFileReaderObj Internal object for reading file.
        VelodyneFileReaderObj;
    end
    
    %==================================================================
    % Custom Getters/Setters
    %==================================================================
    methods
        
        %==================================================================
        % Get CurrentTime property value
        %==================================================================
        function value = get.CurrentTime(this)
            value = this.CurrentTimeInternal;
        end
        
        %==================================================================
        % Set CurrentTime property value
        %==================================================================
        function set.CurrentTime(this, value)
            
            % Check for datatype validity.
            try
                validateattributes(value, {'duration'}, ...
                    {'nonempty', 'scalar'}, 'set', 'CurrentTime');
            catch ME
                throwAsCaller(ME);
            end
            % Check for value finiteness and acceptable limits.
            if (~isfinite(value) || value < this.StartTime || value > this.EndTime)
                error(message('vision:velodyneFileReader:invalidCurrentTime', num2str(seconds(this.StartTime)), num2str(seconds(this.EndTime))));
            end
            this.UserCurrentTimeFlag = true;
            this.CurrentTimeInternal = value;
        end
    end
    
    methods (Access = 'public')
        
        %==================================================================
        % Constructor
        %==================================================================
        function this = velodyneFileReader(fileName, deviceModel, varargin)
            
            % Parse and validate inputs.
            paramsStruct  = parseAndValidateInputs(fileName, deviceModel, varargin{:});
            this.FileName = paramsStruct.FileName;
            
            % Check for input file type.
            [~, ~, fileExtension] = fileparts(fileName);
            if(~strcmpi(fileExtension, '.pcap'))
                error(message('vision:velodyneFileReader:invalidFileType',fileExtension));
            end
            
            % Check if the file exists.
            fid = fopen(this.FileName, 'r');
            if (fid == -1)
                if(~isempty(dir(this.FileName)))
                    error(message('vision:velodyneFileReader:fileReadPermission', this.FileName));
                else
                    error(message('vision:velodyneFileReader:fileDoesNotExist', this.FileName));
                end
            else
                % File exists. Get full filename.
                this.FileName    = fopen(fid);
                fclose(fid);
            end
            
            this.DeviceModel     = paramsStruct.DeviceModel;
            this.CalibrationFile = paramsStruct.CalibrationFile;
            % skipPartialFrames is for internal usage only.
            skipPartialFrames    = paramsStruct.SkipPartialFrames;
            if(isempty(this.CalibrationFile))
                
                if isdeployed
                    rootDirectory = ctfroot;
                else
                    rootDirectory = matlabroot;
                end
                
                defaultCalibrationFile     = fullfile(rootDirectory, 'toolbox', ...
                    'vision', 'visionutilities', 'velodyneFileReaderConfiguration', ...
                    [ char(this.DeviceModel) '.xml']);
                [this.LaserCalibrationData, distanceResolution]  = getVelodyneCorrectionsFromXML(defaultCalibrationFile);
            else
                % Check for input file type.
                [~, ~, fileExtension] = fileparts(this.CalibrationFile);
                if(~strcmpi(fileExtension, '.xml'))
                    error(message('vision:velodyneFileReader:invalidCalibrationFileType', fileExtension));
                end
                
                % Check if xml file exists
                fid = fopen(this.CalibrationFile, 'r');
                if(fid == -1)
                    if(~isempty(dir(this.CalibrationFile)))
                        error(message('vision:velodyneFileReader:fileReadPermission', this.CalibrationFile));
                    else
                        error(message('vision:velodyneFileReader:fileDoesNotExist', this.CalibrationFile));
                    end
                else
                    % File exists.  Get full filename.
                    this.CalibrationFile   = fopen(fid);
                    fclose(fid);
                end
                
                % Read Calibration data from xml file.
                [this.LaserCalibrationData, distanceResolution]  = getVelodyneCorrectionsFromXML(this.CalibrationFile);
                % Number of lasers based on Velodyne device model.
                numLasersOfDeviceModel     = 16;
                if(strcmpi('HDL32E', this.DeviceModel) || strcmpi('VLP32C', this.DeviceModel))
                    numLasersOfDeviceModel = 32;
                elseif(strcmpi('HDL64E', this.DeviceModel))
                    numLasersOfDeviceModel = 64;
                end
                % Validate laser count in calibration data with number of
                % lasers for given device model.
                if(size(this.LaserCalibrationData, 1) ~= numLasersOfDeviceModel)
                    error(message('vision:velodyneFileReader:invalidCalibrationFileIncorrectEnabledLaserCountForDeviceModel', this.DeviceModel, numLasersOfDeviceModel));
                end
            end
            
            % Create the file reader object and open the file
            this.VelodyneFileReaderObj = vision.internal.VelodyneFileReader();
            tmpReturnStruct            = open(this.VelodyneFileReaderObj, this.FileName,...
                struct('LaserCalibrations', this.LaserCalibrationData, 'DistanceResolution', distanceResolution, ...
                'SkipPartialFrames', skipPartialFrames, 'FullFrameAzimuthRangeInDegrees', 358), ...
                this.DeviceModel);
            
            % Fill class properties returned from mex call.
            if(~isempty(tmpReturnStruct))
                this.NumberOfFrames = tmpReturnStruct.NumberOfFrames;
                this.StartTime      = duration(0, 0, tmpReturnStruct.StartTime, 'Format', 's') ;
                this.EndTime        = duration(0, 0, tmpReturnStruct.EndTime, 'Format', 's') ;
                this.Duration       = duration(0, 0, tmpReturnStruct.Duration, 'Format', 's') ;
                
            end
            this.CurrentTimeInternal = this.StartTime;
            this.UserCurrentTimeFlag = false;
        end
        
        %==================================================================
        % Read point cloud frame from velodyneFileReader object
        %==================================================================
        function ptCloudObj = readFrame(this, varargin)
            %readFrame Read a point cloud frame from file
            %
            %   ptCloudObj = readFrame(veloReader) reads the next available
            %   point cloud in sequence. ptCloudObj is a pointCloud object
            %   with the Location specifying the XYZ coordinates of points
            %   (expressed in meters) and Intensity specifying the
            %   intensities of respective points.
            %   The veloReader object keeps track of the last read point
            %   cloud for future calls to readFrame.
            %
            %   ptCloudObj = readFrame(veloReader, frameNumber) reads
            %   point cloud with the specific frame number from the file.
            %   The numeric value, frameNumber, should be a valid positive
            %   number and not more than veloReader.NumberOfFrames.
            %
            %   ptCloudObj = readFrame(veloReader, frameTime)
            %   reads the first point cloud recorded at or after the
            %   given frameTime in seconds. frameTime should be of
            %   duration type.
            %
            %   Example 1: Read point cloud using frame number.
            %   -----------------------------------------------
            %   % Construct velodyneFileReader object.
            %   veloReader = velodyneFileReader('lidarData_ConstructionRoad.pcap', 'HDL32E');
            %
            %   % Read 5th point cloud.
            %   frameNumber = 5;
            %   ptCloudObj  = readFrame(veloReader, frameNumber);
            %
            %   % Display point cloud using pcshow.
            %   figure; pcshow(ptCloudObj);
            %
            %   Example 2: Read point cloud using time duration.
            %   ------------------------------------------------
            %   % Construct velodyneFileReader object.
            %   veloReader = velodyneFileReader('lidarData_ConstructionRoad.pcap', 'HDL32E');
            %
            %   % Create duration object that represents 3 seconds from
            %   % StartTime.
            %   timeDuration = veloReader.StartTime + duration(0, 0, 3, 'Format', 's');
            %
            %   % Read Velodyne point cloud which was recorded at/after
            %   % given time duration from start of the file.
            %   ptCloudObj   = readFrame(veloReader, timeDuration);
            %
            %   % Display point cloud using pcshow.
            %   figure; pcshow(ptCloudObj);
            %
            %   See also  velodyneFileReader, velodyneFileReader/hasFrame,
            %             pcplayer, pointcloud, pcshow.
            
            if(~isempty(varargin))
                if(length(varargin) > 1)
                    error(message('vision:velodyneFileReader:tooManyArgs'));
                else
                    % Check first optional argument type.
                    try
                        validateattributes(varargin{1}, {'numeric', 'duration'}, ...
                            {'nonempty', 'scalar'}, 'readFrame')
                    catch ME
                        error(message('vision:velodyneFileReader:invalidInputArg'));
                    end
                    if(~isfinite(varargin{1}))
                        error(message('vision:velodyneFileReader:invalidInputArg'));
                    end
                    % Check if optional argument is of 'duration' class.
                    if(isduration(varargin{1}))
                        durationToSeek = varargin{1};
                        % Check for valid duration values.
                        if (durationToSeek < this.StartTime || durationToSeek > this.EndTime)
                            error(message('vision:velodyneFileReader:invalidTimeDuration', num2str(seconds(this.StartTime)), num2str(seconds(this.EndTime))));
                        end
                        durationToSeekSeconds                     = double(seconds(durationToSeek - this.StartTime));
                        % Call builtin function with duration in seconds.
                        [xyziPoints, currentTimestamp, rangeData] = readPointCloud(this.VelodyneFileReaderObj, durationToSeekSeconds);
                        
                    elseif(isnumeric(varargin{1})) % Check if optional argument is of 'numeric' class.
                        % Truncate decimal part and keep only integer part.
                        frameNum = int32(floor(varargin{1}));
                        % Check for valid frame number value.
                        if( double(varargin{1}) > double(frameNum) || ...
                                frameNum <= 0 || frameNum > this.NumberOfFrames)
                            error(message('vision:velodyneFileReader:invalidFrameNumber', this.NumberOfFrames));
                        end
                        % Call builtin function with frame number.
                        [xyziPoints, currentTimestamp, rangeData] = readPointCloud(this.VelodyneFileReaderObj, frameNum-1);
                    end
                end
            else
                % Default builtin call if optional arguments not provided.
                if(this.UserCurrentTimeFlag)
                    % If CurrentTime is set by user, use it to retrieve
                    % point cloud.
                    durationToSeekSeconds                     = double(seconds(this.CurrentTimeInternal - this.StartTime));
                    [xyziPoints, currentTimestamp, rangeData] = readPointCloud(this.VelodyneFileReaderObj, durationToSeekSeconds);
                else
                    % If user does not provide CurrentTime, read next point
                    % cloud in sequence.
                    if(hasFrame(this))
                        [xyziPoints, currentTimestamp, rangeData] = readPointCloud(this.VelodyneFileReaderObj, int32(-1));
                    else
                        error(message('vision:velodyneFileReader:endOfFile'));
                    end
                end
            end
            
            ptCloudObj = [];
            if(~isempty(xyziPoints))
                % The laser firing sequence reported in the Velodyne packet
                % is in an order different from the lasers vertical angles
                % (i.e. the order in which lasers are placed/mounted
                % vertically). So, the vertical angles are used to
                % arrange points according to their respective laser's position.
                % Refer to Velodyne Device Manual(s) for more info on this.
                
                % Laser vertical angles are stored in 2nd column of
                % LaserCalibrationData.
                laserVerticalAngles             = this.LaserCalibrationData(:, 2);
                % Sort the vertical angles and obtain indices to sorted
                % vertical angles.
                [~, sortedVerticalAngleIndices] = sort(laserVerticalAngles, 'descend');
                % Create pointCloud object from xyziPoints, with points sorted
                % according to the laser vertical angles.
                ptCloudObj                      = pointCloud(xyziPoints(sortedVerticalAngleIndices, :, 1:3), ...
                    'Intensity', xyziPoints(sortedVerticalAngleIndices, :, 4));
                rangeData                       = rangeData(sortedVerticalAngleIndices, :, :);
                this.CurrentTimeInternal        = this.StartTime + duration(0, 0, currentTimestamp, 'Format', 's') ;
                
                % Convert to radian for angles
                rangeData(:,:,2:3) = rangeData(:,:,2:3) * pi / 180;
                % range, pitch, yaw
                ptCloudObj.RangeData     = rangeData(:,:,[1 3 2]);
            else
                this.CurrentTimeInternal        = this.StartTime + duration(0, 0, 0, 'Format', 's');
            end
            this.UserCurrentTimeFlag = false;
        end
        
        %==================================================================
        % Check if another point cloud is available to read
        %==================================================================
        function flag = hasFrame(this)
            %hasFrame Determine if another point cloud is available
            %
            %   flag = hasFrame(veloReader) returns TRUE if there is a
            %   next point cloud available to read from the file. If not,
            %   it returns FALSE.
            %
            %   Example : Check for next point cloud in the file.
            %   -------------------------------------------------
            %   % Construct velodyneFileReader object.
            %   veloReader = velodyneFileReader('lidarData_ConstructionRoad.pcap', 'HDL32E');
            %
            %   % Check if veloReader has a next point cloud to read.
            %   disp(hasFrame(veloReader));
            %
            %   % Read last frame.
            %   ptCloudObj = readFrame(veloReader,veloReader.NumberOfFrames);
            %
            %   % Check again, if veloReader has a next point cloud available.
            %   disp(hasFrame(veloReader));
            %
            %   See also  velodyneFileReader, velodyneFileReader/readFrame,
            %             pcplayer, pointcloud.
            
            flag = true;
            % Check if timestamp of last frame requested is less than the
            % EndTime of the file.
            % Timestamps in the Velodyne packet are reported in
            % microseconds. If the difference between EndTime and
            % CurrentTimeInterval is less than 1 microsecond (i.e. 1e-6),
            % consider them to be close enough to report reaching last
            % frame, i.e, end of the file reached and next frame
            % unavailable.
            if(abs(seconds(this.EndTime) - seconds(this.CurrentTimeInternal)) < 1e-6)
                flag = false;
            end
        end
        
        %==================================================================
        % Reset velodyneFileReader object to beginning of the file
        %==================================================================
        function reset(this)
            %reset Reset to the beginning of the file
            %
            %   reset(veloReader) resets the status of the veloReader object
            %   to the beginning of the file.
            %
            %   Example : Reset the velodyneFileReader object.
            %   ----------------------------------------------
            %   % Construct velodyneFileReader object.
            %   veloReader = velodyneFileReader('lidarData_ConstructionRoad.pcap', 'HDL32E');
            %
            %   % Loop through all point clouds in the reader.
            %   figure;
            %   while(hasFrame(veloReader))
            %     ptCloudObj = readFrame(veloReader);
            %     pcshow(ptCloudObj);
            %     pause(0.1);
            %   end
            %
            %   % Reset the object.
            %   reset(veloReader);
            %
            %   % Read first frame in the file and display it.
            %   ptCloudObj = readFrame(veloReader);
            %   figure; pcshow(ptCloudObj);
            %
            %   See also  velodyneFileReader, velodyneFileReader/readFrame,
            %             pcplayer, pointcloud.
            
            % Set CurrentTime property to StartTime.
            this.CurrentTime = this.StartTime;
        end
    end
    methods (Hidden)
        %==================================================================
        % clear resources
        %==================================================================
        function delete(this)
            % Call builtin and release resources.
            close(this.VelodyneFileReaderObj);
            % Invalidate class properties.
            this.FileName             = [];
            this.NumberOfFrames       = [];
            this.StartTime            = [];
            this.EndTime              = [];
            this.Duration             = [];
            this.CurrentTimeInternal  = seconds(0);
            this.LaserCalibrationData = [];
            this.DeviceModel          = [];
            this.CalibrationFile      = [];
        end
        
    end
    
    methods(Access = 'protected')
        %==================================================================
        % copy object
        %==================================================================
        function copyObj = copyElement(this)
            % Override copyElement method
            if(~isempty(this.CalibrationFile))
                copyObj = velodyneFileReader(this.FileName, this.DeviceModel, 'CalibrationFile', this.CalibrationFile);
            else
                copyObj = velodyneFileReader(this.FileName, this.DeviceModel);
            end
            copyObj.CurrentTime = this.CurrentTime;
        end
    end
    
    methods(Hidden)
        %==================================================================
        % save object
        %==================================================================
        function s = saveobj(this)
            % save properties into struct
            s.FileName        = this.FileName;
            s.DeviceModel     = this.DeviceModel;
            s.CalibrationFile = this.CalibrationFile;
            s.Version         = this.Version;
            s.CurrentTime     = this.CurrentTime;
        end
    end
    
    methods (Static, Hidden)
        %==================================================================
        % load object
        %==================================================================
        function this = loadobj(s)
            % Load Object
            currentTime = s.CurrentTime;
            if(~isempty(s.CalibrationFile))
                this = velodyneFileReader(s.FileName, s.DeviceModel, 'CalibrationFile', s.CalibrationFile);
            else
                this = velodyneFileReader(s.FileName, s.DeviceModel);
            end
            this.CurrentTime = currentTime;
        end
    end
end

%==================================================================
% parameter validation
%==================================================================
function paramsStruct = parseAndValidateInputs(fileName, deviceModel, varargin)

% SkipPartialFrames PV-Pair is used for internal purposes only.
[flag, skipPartialFrames, varargin] = checkSkipPartialFramesNVPair(varargin{:});
if(flag)
    narginchk(2,6);
else
    narginchk(2,4);
end

% Parse and validate inputs.
p = inputParser;
defaultCalibrationFile = '';

validateattributes(fileName, {'char', 'string'}, {'nonempty'})
validateattributes(deviceModel, {'char', 'string'}, {'nonempty'})
% Set optional parameters.
addParameter(p, 'CalibrationFile', defaultCalibrationFile, @(x)validateattributes(x, {'char', 'string'}, {'nonempty'}))

% Check and parse arguments.
parse(p, varargin{:});
paramsStruct             = p.Results;
paramsStruct.FileName    = fileName;
paramsStruct.DeviceModel = deviceModel;
paramsStruct.SkipPartialFrames = skipPartialFrames;

% Validate device model.
validDeviceModels        = {'VLP16', 'VLP32C', 'HDL32E', 'HDL64E'};
try
    paramsStruct.DeviceModel = validatestring(deviceModel, validDeviceModels);
catch ME
    error(message('vision:velodyneFileReader:invalidVelodyneHDLModel', paramsStruct.DeviceModel));
end

end

%==================================================================
% check for SkipPartialFrames N-V pair for internal usage
%==================================================================
function [flag, skipPartialFrames, vararginMod] = checkSkipPartialFramesNVPair(varargin)
flag = false;
skipPartialFrames = true;
vararginMod = varargin;
str = "skippartialframes";
for i = 1: length(varargin)
    if(isstring(varargin{i}) || ischar(varargin{i}))
        if( strcmp(str, string(varargin{i}).lower))
            if( ((i+1) <= length(varargin)) && islogical(varargin{i+1}))
                flag = true;
                skipPartialFrames = varargin{i+1};
                vararginMod([i i+1]) = [];
                break;
            end
        end
    end
end
end

%==================================================================
% helper function to load laser calibration data from XML file
%==================================================================
function [ laserCorrections, distLSB ] = getVelodyneCorrectionsFromXML(xmlFile)
% Load Velodyne Laser calibration data from XML file.
fid = fopen(xmlFile, 'r');
if (fid == -1)
    error(message('vision:velodyneFileReader:fileDoesNotExist', xmlFile));
else
    % File exists.  Get full filename.
    xmlFile  = fopen(fid);
    fclose(fid);
end

% parse the provided Velodyne laser calibration xml file.
try
    domNode = xmlread(xmlFile);
catch ME
    error(message('vision:velodyneFileReader:calibrationFileReadError'));
end
% Get distLSB_ value
distLSB = 0.2;
distLSBNode = domNode.getElementsByTagName('distLSB_');
if(distLSBNode.getLength() > 0)
    distLSB = getTagValue(domNode,'distLSB_');
end

% Count number of lasers enabled
enabled = domNode.getElementsByTagName('enabled_');
if(enabled.getLength() <= 0)
    error(message('vision:velodyneFileReader:invalidCalibrationFileTagNotFound', ...
        'enabled_'));
end
enabledCount = 0;
for k = 0 : enabled.getLength-1
    enabledItem   = enabled.item(k);
    enabledItemId = enabledItem.getElementsByTagName('item');
    for i= 0 : enabledItemId.getLength()-1
        if(str2double(enabledItemId.item(i).getTextContent) > 0)
            enabledCount = enabledCount+1;
        end
    end
end
if(enabledCount <= 0 ||  ~(enabledCount == 16 || enabledCount == 32 || enabledCount == 64))
    error(message('vision:velodyneFileReader:invalidCalibrationFileIncorrectEnabledLaserCount'));
end
% Read laser corrections
px = domNode.getElementsByTagName('px');
if(px.getLength() <= 0)
    error(message('vision:velodyneFileReader:invalidCalibrationFileTagNotFound', 'px'));
end
if(px.getLength() < enabledCount)
    error(message('vision:velodyneFileReader:invalidCalibrationFileMissingCalibrationValues'));
end
laserCorrections = zeros(enabledCount, 9);
% Read the following tag values into laserCorrections array.
%   <rotCorrection_>-5.3328056</rotCorrection_>
%   <vertCorrection_>-7.2988362</vertCorrection_>
%   <distCorrection_>111</distCorrection_>
%   <distCorrectionX_>118</distCorrectionX_>
%   <distCorrectionY_>118</distCorrectionY_>
%   <vertOffsetCorrection_>19.736338</vertOffsetCorrection_>
%   <horizOffsetCorrection_>2.5999999</horizOffsetCorrection_>
%   <focalDistance_>0</focalDistance_>
%   <focalSlope_>0</focalSlope_>

for k = 0 : enabledCount-1
    pxItem = px.item(k);
    if(pxItem.getLength() <= 0)
        error(message('vision:velodyneFileReader:invalidCalibrationFileTagNotFound', 'px'));
    end
    laserCorrections(k+1, 1) = getTagValue(pxItem, 'rotCorrection_');
    laserCorrections(k+1, 2) = getTagValue(pxItem, 'vertCorrection_');
    laserCorrections(k+1, 3) = getTagValue(pxItem, 'distCorrection_');
    laserCorrections(k+1, 4) = getTagValue(pxItem, 'distCorrectionX_');
    laserCorrections(k+1, 5) = getTagValue(pxItem, 'distCorrectionY_');
    laserCorrections(k+1, 6) = getTagValue(pxItem, 'vertOffsetCorrection_');
    laserCorrections(k+1, 7) = getTagValue(pxItem, 'horizOffsetCorrection_');
    laserCorrections(k+1, 8) = getTagValue(pxItem, 'focalDistance_');
    laserCorrections(k+1, 9) = getTagValue(pxItem, 'focalSlope_');
end
end

%==================================================================
% helper function to parse a numeric tag value for a given XML tag
%==================================================================
function tagValue = getTagValue(pxItem, tagName)
% Utility function to parse, validate and return tag
% value for a given tag in xml file.
pxItemId = pxItem.getElementsByTagName(tagName);
if(pxItemId.getLength() > 0)
    tagValue = str2double(pxItemId.item(0).getTextContent);
    if(isnan(tagValue))
        error(message('vision:velodyneFileReader:invalidCalibrationFileNonnumericTagValue', tagName));
    end
else
    error(message('vision:velodyneFileReader:invalidCalibrationFileTagNotFound', tagName));
end

end

