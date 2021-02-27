function kitchen

room = [-20,-20,0; -20,160,0; 160,160,0; 160,160,160];
figure(1); clf; hold on;
plot3(room(:,1), room(:,2), room(:,3), '.');

CabinetFace = [200/256 200/256 200/256]; % Slate Grey
Countertop = [56/256 56/256 56/256]; % Dark Grey

% Back Wall, Lower cabinet
    lc.BACK.n = [0,0,0; 0,138,0; 0,138,38; 0,0,38];
    lc.BACK.s = [26,26,0; 26,138-26,0; 26,138-26,38; 26,26,38];
    lc.BACK.e = [0,138,0; 0,138,38; 26,138,38; 26,138,0];
    lc.BACK.w = [0,0,0; 26,0,0; 26,0,38; 0,0,38];
    lc.BACK.t = [0,0,38; 0,138,38; 26,138,38; 26,0,38];
    lc.BACK.b = [0,0,0; 0,138,0; 26,138,0; 26,0,0];
    plotpart(lc.BACK, CabinetFace, 'nsewb');
    plotpart(lc.BACK, Countertop, 't');

% Left Wall, Lower cabinet
    LFTlength = 34; % 100
    lc.LEFT.n = [26,0,0; 26,26,0; 26,26,38; 26,0,38];
    lc.LEFT.s = [26+LFTlength,0,0; 26+LFTlength,26,0; 26+LFTlength,26,38; 26+LFTlength,0,38];
    lc.LEFT.e = [26,26,0; 26+LFTlength,26,0; 26+LFTlength,26,38; 26,26,38];
    lc.LEFT.w = [26,0,0; 26+LFTlength,0,0; 26+LFTlength,0,38; 26,0,38];
    lc.LEFT.t = [26,0,38; 26+LFTlength,0,38; 26+LFTlength,26,38; 26,26,38];
    lc.LEFT.b = [26,0,0; 26+LFTlength,0,0; 26+LFTlength,26,0; 26,26,0];
    plotpart(lc.LEFT, CabinetFace, 'nsewb');
    plotpart(lc.LEFT, Countertop, 't');
    
% Right Wall, Lower cabinet
    lc.RHT.n = [26,138,0; 26,138-26,0; 26,138-26,38; 26,138,38];
    lc.RHT.s = [78,138,0; 78,138-26,0; 78,138-26,38; 78,138,38];
    lc.RHT.e = [26,138,0; 78,138,0; 78,138,38; 26,138,38];
    lc.RHT.w = [26,138-26,0; 78,138-26,0; 78,138-26,38; 26,138-26,38];
    lc.RHT.t = [26,138,38; 78,138,38; 78,138-26,38; 26,138-26,38];
    lc.RHT.b = [26,138,0; 78,138,0; 78,138-26,0; 26,138-26,0];
    plotpart(lc.RHT, CabinetFace, 'nsewb');
    plotpart(lc.RHT, Countertop, 't');
    
% Island, Lower cabinet
    offsetval = 52; % minimum 52
    lengthval = 50;
    lc.ISLE.n = [offsetval,112,0; offsetval,112-lengthval,0; offsetval,112-lengthval,38; offsetval,112,38];
    lc.ISLE.s = [offsetval+26,112,0; offsetval+26,112-lengthval,0; offsetval+26,112-lengthval,38; offsetval+26,112,38];
    lc.ISLE.e = [offsetval,112,0; offsetval+26,112,0; offsetval+26,112,38; offsetval,112,38];
    lc.ISLE.w = [offsetval,112-lengthval,0; offsetval+26,112-lengthval,0; offsetval+26,112-lengthval,38; offsetval,112-lengthval,38];
    lc.ISLE.t = [offsetval,112,38; offsetval,112-lengthval,38; offsetval+26,112-lengthval,38; offsetval+26,112,38];
    lc.ISLE.b = [offsetval,112,0; offsetval,112-lengthval,0; offsetval+26,112-lengthval,0; offsetval+26,112,0];
    plotpart(lc.ISLE, CabinetFace, 'nseb');
    plotpart(lc.ISLE, Countertop, 'wt');


view([27 27]);

    function plotpart(in, cabn, sds)
        
        for j=1:length(sds)
            ex = ['fill3(in.' sds(j) '(:,1),in.' sds(j) '(:,2), in.' sds(j) '(:,3), cabn)'];
            eval(ex);
        end
%         fill3(in.e(:,1),in.e(:,2), in.e(:,3), cabn);
%         fill3(in.w(:,1),in.w(:,2), in.w(:,3), cabn);
%         fill3(in.n(:,1),in.n(:,2), in.n(:,3), cabn);
%         fill3(in.s(:,1),in.s(:,2), in.s(:,3), cabn);
%         fill3(in.t(:,1),in.t(:,2), in.t(:,3), ttoopp);
%         fill3(in.b(:,1),in.b(:,2), in.b(:,3), cabn);

    end

end